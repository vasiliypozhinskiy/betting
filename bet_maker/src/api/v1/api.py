import time
import uuid
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
import sqlalchemy as sa

from api.v1.model.request import CreateBetRequest
from api.v1.model.response import BetResponse
from db.db import get_db
from db.postgres.metadata import event_table, bet_table, EVENT_STATES_TO_NUMBERS_MAPPING
from model.model import Event, Bet

router = APIRouter()

EVENT_STATES_ALLOW_TO_BET = {'NEW'}


@router.post('/bet', status_code=HTTPStatus.CREATED)
async def make_bet(bet: CreateBetRequest, db=Depends(get_db)):
    event_for_bet = await db.get_by_id(event_table, bet.event_id)

    if not event_for_bet:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Event for bet not found")
    if event_for_bet.state not in EVENT_STATES_ALLOW_TO_BET:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Event status not allow to bet")
    if event_for_bet.deadline < time.time():
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Betting after deadline")

    new_bet = Bet(id=uuid.uuid4(), event_id=bet.event_id, value=bet.value)
    await db.insert(bet_table, new_bet)

    return new_bet.id


@router.get('/bets')
async def get_bets(db=Depends(get_db)):
    bet_with_event_ids = await db.get_columns(
        table=sa.join(bet_table, event_table, bet_table.c.event_id == event_table.c.id),
        columns=[bet_table.c.id, bet_table.c.event_id, event_table.c.state],
    )

    result = []
    for bet_with_event_id in bet_with_event_ids:
        result.append(
            BetResponse(
                id=bet_with_event_id.id,
                event_id=bet_with_event_id.event_id,
                event_state=EVENT_STATES_TO_NUMBERS_MAPPING[bet_with_event_id.state]
            )
        )

    return result


@router.get('/events')
async def get_events(db=Depends(get_db)):
    rows = await db.get_all(event_table)

    return [Event(id=row.id, state=EVENT_STATES_TO_NUMBERS_MAPPING[row.state]) for row in rows]
