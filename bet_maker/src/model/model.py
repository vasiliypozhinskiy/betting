from decimal import Decimal
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class EventState(Enum):
    NEW = 1
    FINISHED_WIN = 2
    FINISHED_LOSE = 3


class Event(BaseModel):
    id: UUID
    state: EventState


class Bet(BaseModel):
    id: UUID
    event_id: UUID
    value: Decimal

