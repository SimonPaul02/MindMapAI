import logging
import tasks.tangram_models as tangram_models
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


class Tangram(Task):

    def convert_task_data_to_tangram_data(
        self, tangram_data: Any
    ) -> List[tangram_models.Piece]:
        logger.info(tangram_data)
        pieces = []
        for name in tangram_data:
            position_values = tangram_data[name]
            xy_values = position_values[0]
            x = int(xy_values.split(",")[0].replace("(", ""))
            y = int(xy_values.split(",")[1].replace(")", ""))
            position = tangram_models.Position(x=x, y=y, rotation=position_values[1])
            piece = tangram_models.Piece(name=name, position=position)
            pieces.append(piece)
        return pieces

    def process_tangram_data(self, pieces: List[tangram_models.Piece]):
        prompt = "Here are the current positions and rotations of the pieces:\n"
        for piece in pieces:
            prompt += f"{piece.name}: {piece.position.x}, {piece.position.y}, {piece.position.rotation}\n"
        return prompt

    def convert_model_response(self, response: Any) -> tangram_models.Piece:
        try:
            element = json.loads(response)
            name, position_values = list(element.items())[0]
            position = tangram_models.Position(
                x=position_values[0], y=position_values[1], rotation=position_values[2]
            )
            piece = tangram_models.Piece(name=name, position=position)
            return piece
        except:
            logger.error("Error converting model response to Piece")
            return None

    def get_system_prompt(self, objective: str, hasImage: bool = False) -> str:
        """Generate response endpoint:
        generate the response based on given prompt and store the conversation
        in the history of the session (based on the session_id cookie)
        """

        system_prompt = f"""Your are working with a user to solve some task with a tangram puzzle that consists only of two pieces, a small triangle and a square. 
            The stated task is : {objective}
            In each round, you should select one piece and indicate where you want to place it. 
            You will be provided an image with the current placement of all available pieces, no other pieces are available.py
            You might also get some comment by the user on their move.
            If you decide, that the task is fullfilled, tell the user.
            Be brief in your instruction. Instruct the user one step at a time - move one piece in one turn.
            """
        return system_prompt

    def process_model_answer(self, answer: ModelResponse) -> TaskDataResponse:
        # Again, we ignore the potential image here...
        return TaskDataResponse(text=answer.text)

    def generate_model_request(self, request: TaskDataRequest) -> TaskRequest:
        """Generate prompt endpoint:
        process pieces' data and plug them into the prompt
        """
        system_prompt = self.get_system_prompt(request.objective)
        # This could include an image, but for this task, we currently don't supply one
        if request.text == None:
            # Just indicate that it's the AI's turn, TaskRequest has to have non empty Text.
            return TaskRequest(
                text="Your turn", system=system_prompt, image=request.image
            )
        else:
            return TaskRequest(
                text=request.text, system=system_prompt, image=request.image
            )

    def get_requirements(self) -> TaskRequirements:
        return TaskRequirements(needs_text=True, needs_image=True)
