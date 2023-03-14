import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from rabbitmq_clients.consumer import RabbitMQConsumer
from rabbitmq_clients.settings import RabbitMQSettings
from rabbitmq_clients.models import MessageType

from api.v1 import api
from db.postgres.postgres import AsyncPostgres
from core import config
from db import db
from services import consumer

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url='/bet_maker/openapi',
    openapi_url='/bet_maker/openapi.json',
    default_response_class=ORJSONResponse,
)

app.include_router(api.router, prefix='/bet_maker/v1', tags=['bets_and_events'])


@app.on_event('startup')
async def startup():
    consumer.consumer = RabbitMQConsumer(
        settings=RabbitMQSettings(),
        event_handlers={
            MessageType.NEW_EVENT: consumer.on_new_event_handler,
            MessageType.EVENT_CHANGED: consumer.on_event_changed_handler,
        }
     )
    await consumer.consumer.setup()
    await consumer.consumer.setup_queues()
    await consumer.consumer.run()

    pg_connection_params = {
        'user': config.DB_USER,
        'password': config.DB_PASSWORD,
        'database': config.DB_DATABASE,
        'host': config.DB_HOST,
    }

    db.db = AsyncPostgres(pg_connection_params)
    await db.db.setup()


@app.on_event('shutdown')
async def shutdown():
    await consumer.consumer.close()

    db.db.close()


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8080,
        reload=True
    )
