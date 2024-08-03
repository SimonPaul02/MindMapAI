from fastapi import Depends, Request, APIRouter
from routers.router_models import SessionData
from typing import Dict
import time
import hashlib
import grpc
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/session")
channel = grpc.insecure_channel("localhost:8061")

# Mock up sessions db
sessions: Dict[str, SessionData] = {}
"""
sessions[<session_id>] = {
  "history": [ # The history, with the exception of the system message. Contains both user and model messages
    {
      "role": "user"
      "content": <prompt>
    }
  ]
}
"""


def get_session(request: Request) -> SessionData:
    session_id = request.session["key"] if "key" in request.session else None
    if session_id is None or session_id not in sessions:
        session_id = hashlib.sha256(
            (request.client.host + str(time.time())).encode()
        ).hexdigest()
        request.session["key"] = session_id
        sessions[session_id] = SessionData(history=[], id=session_id)
        logger.info(sessions[session_id])
    return sessions[session_id]


def clear_session(request: Request):
    session_id = request.session["key"] if "key" in request.session else None
    if session_id is None or session_id not in sessions:
        pass
    else:
        sessions.pop(session_id)
        return True
