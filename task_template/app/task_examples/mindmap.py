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


class Mindmap(Task):

    def get_system_prompt_mindmap(self, objective: str) -> str:
        """Generate response endpoint:
        generate the response based on given prompt and store the conversation
        in the history of the session (based on the session_id cookie)
        """

        system_prompt = f"""You are a professional, creative writing assistant.
            You are working together with a user to create instructions for this writing task: {objective}. 
            The current instructions are in INSTRUCTIONS and the users question in USER_QUESTION.
            Based on the current instruction and the users question, think about what changes must be done to the instructions.
            Now think about changes that will make the instructions even more creative.
            Adapt the instructions by modifying existing subnodes or generating new subnodes.
            The output format must be a normal JSON file with the same structure as the input file.
            It should be directly parsable. Don't include anything else. 
            """
        return system_prompt

    def get_system_prompt_full_text(self, objective: str) -> str:
        """Generate response endpoint:
        generate the response based on given prompt and store the conversation
        in the history of the session (based on the session_id cookie)
        """

        system_prompt = f"""You are a talented, creative writer capable of crafting content for various topics and formats.
        Your writing task is defined here: {objective}. 
        You receive a JSON file containing the following instructions called INSTRUCTIONS
        Write a creative text based on the Content, Style and Structure from your instructions and return it to the user.
        """
        return system_prompt

    def get_system_prompt_suggestions(self, objective: str) -> str:
        """Generate response endpoint:
        generate the response based on given prompt and store the conversation
        in the history of the session (based on the session_id cookie)
        """

        system_prompt = f"""You are a professional, creative, helpful writing assistant and an expert in this task: {objective}.
            You are working collaboratively together with a user to create instructions for this writing task: {objective}. 
            This is the JSON file with the current instructions: INSTRUCTIONS.
		    Keep your previous SUGGESTIONS in mind, do not repeat yourself over and over again.

             Your are expert {objective}. Please give your  most three valuable suggestions for user about Ihis NSTRUCIONS to improve the outline. 
             Please only reply keep in bullet point format and each point keep one simple sentence without other information.

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

        if (request.inputData["handlerID"] == 1):
            return TaskRequest(
                text=f"[INSTRUCTIONS] : {request.inputData['mindMap']} \n[SUGGESTIONS] : {request.inputData['suggestions']} \n[USER_QUESTION] : {request.text}",
                system=self.get_system_prompt_mindmap(request.objective),
                image=None,
            )
        elif (request.inputData["handlerID"] == 2):
            return TaskRequest(
                text=f"[INSTRUCTIONS] : {request.inputData['mindMap']}",
                system=self.get_system_prompt_full_text(request.objective),
                image=None,
            )
        else:
            return TaskRequest(
            text=f"[INSTRUCTIONS] : {request.inputData['mindMap']},\n [SUGGESTIONS] : {request.inputData['suggestions']} ",
            system=self.get_system_prompt_suggestions(request.objective),
            image=None,
        )

    def get_requirements(self) -> TaskRequirements:
        return TaskRequirements(needs_text=True, needs_image=False)

