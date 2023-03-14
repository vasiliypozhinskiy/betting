from rabbitmq_clients.models import MessageType, EventMessage

from model.event import Event

publisher = None


async def on_create_event(event: Event):
    await publisher.publish(
        EventMessage(id=event.id, state=event.state.value, deadline=event.deadline), MessageType.NEW_EVENT
    )


async def on_update_event(event: Event):
    await publisher.publish(
        EventMessage(id=event.id, state=event.state.value, deadline=event.deadline), MessageType.EVENT_CHANGED
    )
