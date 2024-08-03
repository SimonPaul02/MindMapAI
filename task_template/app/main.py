from fastapi import FastAPI, Request
import logging
import logging.config
import configparser
from routers.task_router import task_router, task_handler
from routers.session import router as session_router
from grpc_server import task_server
from starlette.middleware.sessions import SessionMiddleware
import secrets
import concurrent.futures

# This will need to be adapted by the individual task!
from tasks.task import task as current_task

# Set the logger config
logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

task_handler.set_Task(current_task)
logger = logging.getLogger("app")
# Router handling.
app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=secrets.token_hex(32), max_age=None)
logger.info("Session middleware added")
app.include_router(task_router)
app.include_router(session_router)


@app.middleware("http")
async def logger_middleware(request: Request, call_next):
    path = request.url.path
    method = request.method
    log_message = f"Received request: {method} {path}"
    logger.info(log_message)
    logger.info(request.headers)
    response = await call_next(request)
    return response


# Serve the frontend
from static_files import SPAStaticFiles

app.mount("/", SPAStaticFiles(directory="dist", html=True), name="FrontEnd")


# Start the GRPC Server
import grpc.aio as grpc
import asyncio
import grpc_server.tasks_pb2_grpc as task_pb2_grpc
import grpc_server.task_server as task_server
from grpc_server.queue_handler import queue_handler


async def grpc_server():
    port = 8061
    # create a grpc server :
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    task_pb2_grpc.add_taskServiceServicer_to_server(
        task_server.TaskServicer(queue_handler), server
    )
    logger.info("Starting GRPC server. Listening on port : " + str(port))
    server.add_insecure_port("0.0.0.0:{}".format(port))
    await server.start()
    await server.wait_for_termination()


loop = asyncio.get_event_loop()
loop.create_task(grpc_server())
