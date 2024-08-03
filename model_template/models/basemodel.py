import model_pb2
from data_models import *


class AIModel:
    def get_model_definition(self) -> model_pb2.modelDefinition:
        raise NotImplementedError()

    def publish_metrics(self, metrics_json: str) -> None:
        raise NotImplementedError()

    async def get_response(self, message: TaskInput) -> TaskOutput:
        raise NotImplementedError()
