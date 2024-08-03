from typing import Any, List, Optional
from pydantic import BaseModel, Field


class TaskDataRequest(BaseModel):
    # Regular input
    text: Optional[str] = None
    inputData: Any
    image: Optional[str] = None
    objective: Optional[str] = None
  


class TaskRequest(BaseModel):
    # The text of the request
    text: Optional[str] = Field(default="", nullable=True)
    # the image of the request
    image: Optional[str] = Field(default=None, nullable=True)
    # The system message of the request
    system: str


class ModelResponse(BaseModel):
    # The text of the request
    text: str
    # the image of the request
    image: Optional[str] = Field(default=None, nullable=True)


class TaskDataResponse(BaseModel):
    text: Optional[str] = None
    image: Optional[str] = None
    outputData: Optional[Any] = None


class TaskRequirements(BaseModel):
    needs_text: bool
    needs_image: bool
    multirequest: Optional[bool] = Field(default=False)


class TaskMetrics(BaseModel):
    metrics: Any
