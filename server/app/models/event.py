from pydantic import BaseModel
from datetime import datetime
from typing import Any


class GameEvent(BaseModel):
    type: str
    source: str
    payload: dict[str, Any]
    timestamp: datetime = None
