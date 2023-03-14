from decimal import Decimal

from pydantic import BaseModel, validator

from model.event import EventState


class UpdateEventRequest(BaseModel):
    coefficient: Decimal
    deadline: int
    state: EventState

    @validator('coefficient')
    def check_value(cls, coefficient: Decimal) -> Decimal:
        if coefficient <= 0:
            raise ValueError('Coefficient must be positive')
        return coefficient


class CreateEventRequest(BaseModel):
    coefficient: Decimal
    deadline: int

    @validator('coefficient')
    def check_value(cls, coefficient: Decimal) -> Decimal:
        if coefficient <= 0:
            raise ValueError('Coefficient must be positive')
        return coefficient
