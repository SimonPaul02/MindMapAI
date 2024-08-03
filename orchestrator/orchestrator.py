import orchestrator_pb2 as pb2
import orchestrator_pb2_grpc as grpc_pb2


import grpc.aio as agrpc
import grpc

import asyncio

import logging
import logging.config

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

logger = logging.getLogger("app")

task_channel_port = 8061
model_handler_port = 8061
model_port = 8061

task_channel = grpc.insecure_channel(f"task_template:{task_channel_port}")
model_channel = grpc.insecure_channel(f"model_template:{model_port}")
model_handler_channel = grpc.insecure_channel(
    f"model_handler_template:{model_handler_port}"
)


task_stub = grpc_pb2.taskServiceStub(task_channel)
model_stub = grpc_pb2.ModelStub(model_channel)
model_handler_stub = grpc_pb2.ModelHandlerStub(model_handler_channel)

task_receivers = {}
model_receivers = {}
model_handler_receivers = {}


def start_model_handling():
    # Register the model
    model_request = pb2.Empty()
    modelDef = model_stub.registerModel(model_request)
    done = model_handler_stub.registerModel(modelDef)


async def start_task(stub):
    task_request = pb2.Empty()
    tasks = stub.startTask(task_request)
    async for task in tasks:
        logger.info("Starting task with")
        model_handler_stub.startTask(task)


async def run_Task(stub):
    task_request = pb2.Empty()
    taskRequests = stub.runTask(task_request)
    async for taskRequest in taskRequests:
        logger.info("Running task with")
        model_request = model_handler_stub.sendToModel(taskRequest)
        logger.info("Sending to model")
        model_stub.predict(model_request)


async def finish_task(stub):
    task_request = pb2.Empty()
    finishTasks = stub.finishTask(task_request)
    async for finishRequest in finishTasks:
        logger.info("Finishing task with:")
        metrics = model_handler_stub.finishTask(finishRequest)
        model_stub.publishMetrics(metrics)


async def returnPrediction(stub):
    logger.info("Looping over prediction returns")
    model_request = pb2.Empty()
    logger.info("Initializing Model")
    model_predictions = stub.sendPrediction(model_request)
    async for prediction in model_predictions:
        logger.info("Returning prediction:")
        prediction = model_handler_stub.returnToTask(prediction)
        task_stub.getModelResponse(prediction)
    logger.info("Finished looping")


logger.info(task_receivers)


async def main():
    async_task_channel = agrpc.insecure_channel(f"task_template:{task_channel_port}")
    async_model_channel = agrpc.insecure_channel(f"model_template:{model_port}")
    async_model_handler_channel = agrpc.insecure_channel(
        f"model_handler_template:{model_handler_port}"
    )
    async_task_stub = grpc_pb2.taskServiceStub(async_task_channel)
    async_model_stub = grpc_pb2.ModelStub(async_model_channel)
    ## When these all return, the servers are ready.
    await async_task_channel.channel_ready()
    await async_model_channel.channel_ready()
    await async_model_handler_channel.channel_ready()
    # At this point everything should be up.
    # We can now start the model handling
    start_model_handling()
    logger.info("Model Handler started")
    await asyncio.gather(
        start_task(async_task_stub),
        run_Task(async_task_stub),
        finish_task(async_task_stub),
        returnPrediction(async_model_stub),
    )


asyncio.run(main())
