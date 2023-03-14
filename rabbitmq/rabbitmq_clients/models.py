from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class MessageType(Enum):
    NEW_EVENT = 'new_event'
    EVENT_CHANGED = 'event_changed'


class EventState(Enum):
    NEW = 1
    FINISHED_WIN = 2
    FINISHED_LOSE = 3


class EventMessage(BaseModel):
    id: UUID
    deadline: int
    state: EventState
