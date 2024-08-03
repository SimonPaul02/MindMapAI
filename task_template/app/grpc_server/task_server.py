import grpc_server.tasks_pb2_grpc as tasks_pb2_grpc
import grpc_server.tasks_pb2 as tasks_pb2
import queue
import logging
import traceback
import grpc_server.queue_handler as queue_handler
import asyncio
import grpc

required_properties = tasks_pb2.modelRequirements()
required_properties.needs_text = True
required_properties.needs_image = False

logger = logging.getLogger("app")


class TaskServicer(tasks_pb2_grpc.taskServiceServicer):
    def __init__(
        self,
        queue_handler: queue_handler.QueueHandler,
    ):
        self.queue_handler = queue_handler

    async def startTask(self, request, context):
        logger.info("Starting queue for task starts")
        _ = request
        while True:
            try:
                # with timeout to permit detection of interrupted connection
                if self.queue_handler.start_queue.empty():
                    await asyncio.sleep(1)
                else:
                    job = self.queue_handler.start_queue.get()
                    logger.info("Starting task with data:")
                    logger.info(job)
                    self.queue_handler.response_queues[job.sessionID] = queue.Queue()
                    yield job

            except Exception as e:
                logger.info("exception in startTask: %s\n%s", e, traceback.format_exc())
                # allow new call to start
                break

    async def runTask(self, request, context):
        _ = request
        logger.info("Starting queue to run tasks starts")
        while True:
            try:
                # with timeout to permit detection of interrupted connection
                if self.queue_handler.task_queue.empty():
                    await asyncio.sleep(1)
                else:
                    job = self.queue_handler.task_queue.get(timeout=0.1)
                    logger.info(job)
                    yield job

            except Exception as e:
                logging.info("exception in runTask: %s\n%s", e, traceback.format_exc())
                # allow new call to start
                break

    async def finishTask(self, request, context):
        # get the value of the response by calling the desired function :
        _ = request
        logger.info("Starting queue to finish tasks")
        while True:
            try:
                # with timeout to permit detection of interrupted connection
                if self.queue_handler.finish_queue.empty():
                    await asyncio.sleep(1)
                else:
                    data = self.queue_handler.finish_queue.get(timeout=0.1)
                    logger.info("Finishing tasktask")
                    job = tasks_pb2.taskMetrics()
                    job.sessionID = data["sessionID"]
                    job.metrics = data["metrics"]
                    yield job

            except Exception as e:
                logging.info(
                    "exception in finishTask: %s\n%s", e, traceback.format_exc()
                )
                # allow new call to start
                break

    def getModelResponse(self, request, context):
        logger.info("Received response from model")
        if request.sessionID in self.queue_handler.response_queues:
            current_queue = self.queue_handler.response_queues[request.sessionID]
            current_queue.put(request)
        else:
            logging.error(
                "Session ID not found in response_queues, couldn't hanlde request"
            )
        return tasks_pb2.Empty()
