from aio_pika import Message

from .base_client import BaseRabbitMQClient
from .models import EventMessage, MessageType


class RabbitMQPublisher(BaseRabbitMQClient):
    async def publish(self, message: EventMessage, type: MessageType) -> None:
        await self.exchange.publish(
            routing_key=self.make_routing_key(type),
            message=Message(message.json().encode()),
        )
