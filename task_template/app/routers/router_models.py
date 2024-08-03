from typing import Any, List, Optional
from pydantic import BaseModel


class ConversationItem(BaseModel):
    role: str
    content: str


class SessionData(BaseModel):
    history: List[ConversationItem]
    id: str


class TaskRequest(BaseModel):
    text: List[ConversationItem]
    image: Optional[str] = None
    system: str
