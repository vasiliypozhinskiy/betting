from uuid import UUID

from pydantic import BaseModel

from model.model import EventState


class BetResponse(BaseModel):
    id: UUID
    event_id: UUID
    event_state: EventState


class BetsResponse(BaseModel):
    bets: list[BetResponse]