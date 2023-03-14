from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, validator


class CreateBetRequest(BaseModel):
    event_id: UUID
    value: Decimal

    @validator('value')
    def check_value(cls, value: Decimal) -> Decimal:
        if value <= 0:
            raise ValueError('Value must be positive')
        return value

