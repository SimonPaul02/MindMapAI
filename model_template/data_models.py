from pydantic import BaseModel, Field
from typing import List, Optional


class TaskMessage(BaseModel):
    role: str  # The role of the Message (either "assistant" or "user")
    content: str  # The content of the message


class TaskInput(BaseModel):
    text: List[TaskMessage]  # The history of the conversation
    image: Optional[str] = Field(
        default=None, nullable=True
    )  # The image to be processed
    system: Optional[str] = Field(
        default=""
    )  # A System message that indicates the Task


class TaskOutput(BaseModel):
    text: str = Field(default="", nullable=True)  # The response Message
    image: str = Field(default=None, nullable=True)  # The image to be processed
