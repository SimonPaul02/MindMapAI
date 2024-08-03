import logging
from typing import Any, List
import json
from tasks.task_interface import Task
from models import (
    TaskDataRequest,
    TaskRequest,
    TaskDataResponse,
    ModelResponse,
    TaskRequirements,
)

logger = logging.getLogger(__name__)


class Suggestions(Task):

    def get_system_prompt(self, objective: str) -> str:
        """Generate response endpoint:
        generate the response based on given prompt and store the conversation
        in the history of the session (based on the session_id cookie)
        """

        system_prompt = f"""You are a professional, creative, helpful writing assistant and an expert in this task: {objective}.
            You are working collaboratively together with a user to create instructions for this writing task: {objective}. 
            This is the JSON file with the current instructions: INSTRUCTIONS.

            You are supposed to return a list of precise feedback in the following order:
            Short greeting.
            Identify a weakness or problems in the current instructions. How might the user solve this?
            Think of any additional content or style/structure constraints that are missing. Give some hints about them.
            Ask the a question that encourages the user to be creative and think out of the box.
            Encourage the user a little.
            """
        return system_prompt

    def process_model_answer(self, answer: ModelResponse) -> TaskDataResponse:
        # Again, we ignore the potential image here...
        return TaskDataResponse(text=answer.text)

    def generate_model_request(self, request: TaskDataRequest) -> TaskRequest:
        """Generate prompt endpoint:
        process pieces' data and plug them into the prompt
        """
        # This could include an image, but for this task, we currently don't supply one
        logger.info(request)
        return TaskRequest(
            text=f"[INSTRUCTIONS] : {request.inputData['mindMap']},[SUGGESTIONS] : {request.inputData['suggestions']} ",
            system=self.get_system_prompt(request.objective),
            image=None,
        )

    def get_requirements(self) -> TaskRequirements:
        return TaskRequirements(needs_text=True, needs_image=False)
