from typing import Callable

from aio_pika import IncomingMessage

from .base_client import BaseRabbitMQClient
from .models import MessageType, EventMessage
from .settings import RabbitMQSettings

EVENT_HANDLER_TYPE = Callable[[EventMessage], None]


class RabbitMQConsumer(BaseRabbitMQClient):
    def __init__(
        self,
        settings: RabbitMQSettings,
        event_handlers: dict[MessageType, EVENT_HANDLER_TYPE],
    ) -> None:
        super().__init__(settings=settings)
        self.event_handlers = event_handlers
        self.queues_to_handlers = []

    async def setup_queues(self) -> None:
        for event, handler in self.event_handlers.items():
            queue = await self.channel.declare_queue(name=str(event))
            await queue.bind(
                exchange=self.settings.exchange,
                routing_key=self.make_routing_key(event),
            )

            self.queues_to_handlers.append((queue, handler))

    async def run(self) -> None:
        try:
            for queue, handler in self.queues_to_handlers:
                await queue.consume(
                    callback=self.make_callback(handler),
                    no_ack=True,
                )
        except KeyboardInterrupt:
            await self.connection.close()

    @staticmethod
    def make_callback(event_handler: EVENT_HANDLER_TYPE) -> Callable:
        async def on_message_callback(
            message: IncomingMessage,
        ) -> None:
            message = EventMessage.parse_raw(message.body)
            await event_handler(message)

        return on_message_callback
