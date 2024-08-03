import grpc.aio as grpc
from concurrent import futures
import asyncio
import random

# import the generated classes :
import model_handler_pb2
import model_handler_pb2_grpc

port = 8061


class ModelHandler(model_handler_pb2_grpc.ModelHandlerServicer):
    def __init__(self):
        self.model_list = (
            []
        )  # a list of all the modelDefinition that got registered to the handler
        self.assignment_list = (
            {}
        )  # a dictionary for storing the modelID-sessionID connection

    def startTask(self, request, context):
        suitable_models_list = []

        modelRequirements = {
            "needs_text": request.needs_text,
            "needs_image": request.needs_image,
            "sessionID": request.sessionID,
        }

        # Scan in the model list for the suitable model
        for model in self.model_list:
            if modelRequirements["needs_text"] and modelRequirements["needs_image"]:
                if model["can_text"] and model["can_image"]:
                    suitable_models_list.append(model)
            elif modelRequirements["needs_text"]:
                if model["can_text"] and not model["needs_image"]:
                    suitable_models_list.append(model)
            elif modelRequirements["needs_image"]:
                if model["can_image"] and not model["needs_text"]:
                    suitable_models_list.append(model)

        # choose a random model if there are multiple that sastisfy the requirements
        chosen_model = random.choice(suitable_models_list)
        print("The chosen model is")
        print(chosen_model)

        # connect the modelID to the sessionID
        self.assignment_list[modelRequirements["sessionID"]] = chosen_model["modelID"]

        return model_handler_pb2.Empty()

    def finishTask(self, request, context):
        taskMetrics = request
        modelID = self.assignment_list[taskMetrics.sessionID]

        # Break the model assignment after sending the metrics
        del self.assignment_list[taskMetrics.sessionID]

        return model_handler_pb2.metricsJson(
            metrics=taskMetrics.metrics, modelID=modelID
        )

    def sendToModel(self, request, context):
        taskRequest = request
        modelID = self.assignment_list[taskRequest.sessionID]

        return model_handler_pb2.modelRequest(
            request=taskRequest.request,
            modelID=modelID,
            sessionID=taskRequest.sessionID,
        )

    def returnToTask(self, request, context):
        modelAnwer = request

        return model_handler_pb2.modelAnswer(
            answer=modelAnwer.answer, sessionID=modelAnwer.sessionID
        )

    def registerModel(self, request, context):
        print("===Register a model===")
        print(request)
        modelDefinition = {
            "needs_text": request.needs_text,
            "needs_image": request.needs_image,
            "can_text": request.can_text,
            "can_image": request.can_image,
            "modelID": request.modelID,
        }

        self.model_list.append(
            modelDefinition
        )  # add the models to the model list on startup
        return model_handler_pb2.Empty()


async def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    model_handler_pb2_grpc.add_ModelHandlerServicer_to_server(ModelHandler(), server)
    print("Starting the model handler server. Listening on port : " + str(port))
    server.add_insecure_port("0.0.0.0:{}".format(port))
    await server.start()
    await server.wait_for_termination()


asyncio.run(serve())
