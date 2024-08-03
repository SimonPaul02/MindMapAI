from models import (
    TaskDataRequest,
    TaskDataResponse,
    TaskRequest,
    ModelResponse,
    TaskRequirements,
)
from typing import Union, List

class Task:
    def __init__(self):
        pass

    def generate_model_request(
        self,
        request: TaskDataRequest,
    ) -> TaskRequest:
        raise NotImplementedError()

    def process_model_answer(self, answer: ModelResponse) -> TaskDataResponse:
        raise NotImplementedError()

    def get_requirements(self) -> TaskRequirements:
        raise NotImplementedError()
