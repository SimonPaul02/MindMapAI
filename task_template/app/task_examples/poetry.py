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


class Poetry(Task):

    def get_system_prompt(self, objective: str) -> str:
        """Generate response endpoint:
        generate the response based on given prompt and store the conversation
        in the history of the session (based on the session_id cookie)
        """

        system_prompt = f"""You are working together with a user to iteratively create a poem. 
            The details of the poem are as follows : {objective}
            Each of you should generate one line in each step. You will get a message from the user in the form 
            POEM_LINE COMMENT_LINE: POEM_LINE is the new poem line provided by the user and it is 
            wrapped inside square brackets while COMMENT_LINE are the comment made by the user.
            Your answer should take the comment and the poem line into consideration.
            If the COMMENT_LINE and a POEM_LINE are both empty, it means they want you to start the poem, 
            and you must answer by generating the first line of poem, wrapped inside square brackets: (example:
            "[In a golden sky, the sun starts to set]").
            If the COMMENT_LINE is not empty and the POEM_LINE is empty, you give your 
            opinion or answer about the content of COMMENT_LINE that the user provided (example: "I like the poem so far, 
            it depicts a beautiful picture"). If the user ask a question, you anser it.
            Otherwise, your answer must follow this form: [YOUR_POEM_LINE] [YOUR_COMMENT] where 
            YOUR_POEM_LINE is the poem line you created and it has to be wrapped inside square brackets while YOUR_COMMENT
            is your answer or opinion about the content of COMMENT_LINE that the user provided provided in normal text form (example:
            "[In a golden sky, the sun starts to set] I like the idea of a golden sky in the sun set"). You should say your
            feeling about the poem line the user gave and give recommendation about it if needed.
            You are curious, and always ready and eager to ask the user question if needed.
            Your poem line must not repeat what the user has already given, or what you have generated before.
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
            # text update: MAP_DATA + TEXT_INPURT + LATEST_OUTPUT + LATEST_SUGGESTION
            # text=f"[MAP_DATA] : {request.mapData} \n [TEXT_INPUT] : {request.text} \n [LATEST_OUTPUT] : {request.latestOuput} \n [LATEST_SUGGESTION] : {request.latestSuggestion}"
            # system=self.get_system_prompt(request.objective),
            # image=None,
            text=f"[POEM_LINE] : {request.text} \n[COMMENT_LINE] : {request.inputData['commentData']}",
            system=self.get_system_prompt(request.objective),
            image=None,
        )

    def get_requirements(self) -> TaskRequirements:
        return TaskRequirements(needs_text=True, needs_image=False)
