import time
import uuid

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from rabbitmq_clients.publisher import RabbitMQPublisher
from rabbitmq_clients.settings import RabbitMQSettings

from api.v1 import event
from core import config
from db.in_memory import InMemoryDB
from db import db
from services import publisher
from model.event import EventState, Event
from services.publisher import on_create_event

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url='/line_provider/openapi',
    openapi_url='/line_provider/openapi.json',
    default_response_class=ORJSONResponse,
)

app.include_router(event.router, prefix='/line_provider/v1/event', tags=['event'])

initial_events = [
    Event(id=None, coefficient=1.2, deadline=int(time.time()) + 600, state=EventState.NEW),
    Event(id=None, coefficient=1.15, deadline=int(time.time()) + 60, state=EventState.NEW),
    Event(id=None, coefficient=1.67, deadline=int(time.time()) + 90, state=EventState.NEW)
]


@app.on_event('startup')
async def startup():
    publisher.publisher = RabbitMQPublisher(settings=RabbitMQSettings())
    await publisher.publisher.setup()

    db.db = InMemoryDB()
    for event in initial_events:
        db.db.insert_event(event)
        await on_create_event(event)


@app.on_event('shutdown')
async def shutdown():
    await publisher.publisher.close()


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8080,
        reload=True
    )