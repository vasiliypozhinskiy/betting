import time
from http import HTTPStatus

from fastapi import APIRouter, Path, HTTPException, Depends, BackgroundTasks

from api.v1.model.request import CreateEventRequest, UpdateEventRequest
from db.db import get_db
from model.event import EventState, Event
from services.publisher import on_create_event, on_update_event

router = APIRouter()


@router.post('/')
async def create_event(event_data: CreateEventRequest, tasks: BackgroundTasks, db=Depends(get_db)):
    delay = event_data.deadline - time.time()
    if delay < 0:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Wrong deadline")

    new_event = Event(
        id=None,
        coefficient=event_data.coefficient,
        deadline=event_data.deadline,
        state=EventState.NEW
    )

    db.insert_event(new_event)
    tasks.add_task(on_create_event, new_event)

    return HTTPStatus.CREATED


@router.put('/{event_id}')
async def update_event(
        event: UpdateEventRequest,
        tasks: BackgroundTasks,
        event_id: str = Path(default=None),
        db=Depends(get_db)
):
    events = db.get_all_events()
    if event_id not in events:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Event not found")

    db.update_event(event_id, event)
    tasks.add_task(
        on_update_event,
        Event(id=event_id, coefficient=event.coefficient, deadline=event.deadline, state=event.state)
    )

    return HTTPStatus.OK


@router.get('/{event_id}')
async def get_event(event_id: str = Path(default=None), db=Depends(get_db)):
    event = db.get_event_by_id(event_id)
    if not event:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Event not found")

    return event


@router.get('/')
async def get_events(db=Depends(get_db)):
    events = db.get_all_events()
    return list(e for e in events.values() if time.time() < e.deadline)
