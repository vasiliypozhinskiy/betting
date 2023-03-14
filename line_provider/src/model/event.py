from typing import Optional
from decimal import Decimal
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class EventState(Enum):
    NEW = 1
    FINISHED_WIN = 2
    FINISHED_LOSE = 3


class Event(BaseModel):
    id: Optional[UUID]
    coefficient: Decimal
    deadline: int
    state: EventState
