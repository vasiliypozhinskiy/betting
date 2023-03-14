import time
import uuid
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from api.v1.model.request import CreateBetRequest
from api.v1.model.response import BetResponse
from db.db import get_db
from db.postgres.metadata import event_table, bet_table, EVENT_STATES_TO_NUMBERS_MAPPING
from model.model import Event, Bet

router = APIRouter()

EVENT_STATES_ALLOW_TO_BET = {'NEW'}


@router.post('/bet', status_code=HTTPStatus.CREATED)
async def make_bet(bet: CreateBetRequest, db=Depends(get_db)):
    event_rows = await db.get_all(event_table)
    event_for_bet = list(filter(lambda event: event.id == bet.event_id, event_rows))

    if not len(event_for_bet):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Event for bet not found")
    if event_for_bet[0].state not in EVENT_STATES_ALLOW_TO_BET:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Event status not allow to bet")
    if event_for_bet[0].deadline < time.time():
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Betting after deadline")

    new_bet = Bet(id=uuid.uuid4(), event_id=bet.event_id, value=int(bet.value * 100))
    await db.insert(bet_table, new_bet)

    return new_bet.id


@router.get('/bets')
async def get_bets(db=Depends(get_db)):
    bets = await db.get_all(bet_table)

    result = []
    for bet in bets:
        event = await db.get_by_id(event_table, bet.event_id)
        result.append(
            BetResponse(id=bet.id, event_id=bet.event_id, event_state=EVENT_STATES_TO_NUMBERS_MAPPING[event.state])
        )

    return result


@router.get('/events')
async def get_events(db=Depends(get_db)):
    rows = await db.get_all(event_table)

    return [Event(id=row.id, state=EVENT_STATES_TO_NUMBERS_MAPPING[row.state]) for row in rows]
