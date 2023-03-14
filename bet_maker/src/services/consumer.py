from db.db import get_db
from db.postgres.metadata import event_table, NUMBERS_TO_EVENT_STATES_MAPPING
from rabbitmq_clients.models import EventMessage

consumer = None


async def on_new_event_handler(event: EventMessage):
    db = get_db()
    await db.insert(
        event_table,
        {
            'id': event.id,
            'deadline': event.deadline,
            'state': NUMBERS_TO_EVENT_STATES_MAPPING[event.state.value]
        }
    )


async def on_event_changed_handler(event: EventMessage):
    db = get_db()

    await db.update(
        event_table,
        event.id,
        {
            'deadline': event.deadline,
            'state': NUMBERS_TO_EVENT_STATES_MAPPING[event.state.value]
        }
    )
