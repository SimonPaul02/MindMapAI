import grpc.aio as grpc
from concurrent import futures

# import the generated classes :
import model_pb2
import model_pb2_grpc

# import the function we made :
from model import ai_model
import asyncio
import queue
from data_models import TaskInput
import logging
import logging.config

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

logger = logging.getLogger("app")

port = 8061


# create a class to define the server functions, derived from
class ModelServicer(model_pb2_grpc.ModelServicer):
    def __init__(self, ai_model=ai_model, testing=False):
        self.start_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.ai_model = ai_model
        self.testing = testing
        self.called = 0
        if testing:
            self.discard_queue = queue.Queue()

    def publishMetrics(self, request, context):
        logger.info("Publishing metrics")
        logger.info(request)
        if self.ai_model.get_model_definition().modelID != request.modelID:
            if self.testing:
                self.discard_queue.put(request)
            # Not sure, whether we need to abort, as this might caus esome unexpected error.
            # This is just not connected to anything...
            # context.abort(StatusCode.UNIMPLEMENTED, "You've reached the wrong service.")
            return model_pb2.Empty()
        # We will just have the model print the metrics
        self.ai_model.publish_metrics(request.metrics)
        return model_pb2.Empty()

    def predict(self, request, context):
        logger.info("Predicting")
        logger.info(request)
        if self.ai_model.get_model_definition().modelID != request.modelID:
            logger.info("Wrong model, skipping")
            if self.testing:
                self.discard_queue.put(request)
            # Not sure, whether we need to abort, as this might caus esome unexpected error.
            # This is just not connected to anything...
            # context.abort(StatusCode.UNIMPLEMENTED, "You've reached the wrong service.")
            return model_pb2.Empty()
        # define the buffer of the response :
        # get the value of the response by calling the desired function :
        logger.info("Correct model, putting request to the queue")
        self.start_queue.put(request)
        return model_pb2.Empty()

    async def do_prediction(self, data: model_pb2.modelRequest):
        try:
            logger.info(data.request)
            input = TaskInput.model_validate_json(data.request)
            logger.info("Sending request to model")
            logger.info(input)
            result = await self.ai_model.get_response(input)
            logger.info("Got response from model")
            logger.info(result)
            modelAnswer = model_pb2.modelAnswer()
            modelAnswer.answer = result.model_dump_json()
            modelAnswer.sessionID = data.sessionID
            logger.info("Putting response to result queue")
            self.result_queue.put(modelAnswer)
        except Exception as e:
            logger.error(e)

    async def process_queue(self):
        try:
            while True:
                if self.start_queue.empty():
                    # logger.info("Start queue still empty, waiting...")
                    await asyncio.sleep(1)
                else:
                    data = self.start_queue.get(timeout=1.0)
                    # logger.info("Processing Request")
                    # logger.info(data)
                    task = asyncio.create_task(self.do_prediction(data))
        except Exception as e:
            logger.info(e)

    async def sendPrediction(self, request, context):
        try:
            _ = request
            logger.info("Starting prediction queue")
            asyncio.create_task(self.process_queue())
            try:
                while True:
                    if self.result_queue.empty():
                        # logger.info("Prediction queue empty, waiting...")
                        await asyncio.sleep(1)
                    else:
                        # logger.info("Sending response")
                        data = self.result_queue.get(timeout=1.0)
                        yield data
            except Exception as e:
                logger.info(e)
        except Exception as e:
            logger.info(e)
        logger.info("Stopping prediction queue...")

    def registerModel(self, request, context):
        logger.info("Registering model")
        logger.info(request)
        if self.called > 0:
            context.set_code(grpc.StatusCode.OUT_OF_RANGE)
        self.called += 1
        return self.ai_model.get_model_definition()


async def serve():
    # create a grpc server :
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    model_pb2_grpc.add_ModelServicer_to_server(ModelServicer(), server)
    logger.info("Starting server. Listening on port : " + str(port))
    server.add_insecure_port("0.0.0.0:{}".format(port))
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())
