from typing import Any, List, Optional
from pydantic import BaseModel


class ChatMessage(BaseModel):
    message: str


class Position(BaseModel):
    x: float
    y: float
    rotation: int


class Piece(BaseModel):
    name: str
    position: Position
