import aio_pika
import backoff
from aiormq import AMQPConnectionError

from .models import MessageType
from .settings import RabbitMQSettings


class BaseRabbitMQClient:
    connection: aio_pika.Connection
    channel: aio_pika.Channel
    exchange: aio_pika.Exchange

    def __init__(self, settings: RabbitMQSettings) -> None:
        self.settings = settings

    @backoff.on_exception(
        wait_gen=backoff.expo,
        exception=AMQPConnectionError,
        max_tries=5,
    )
    async def setup(self) -> None:
        self.connection = await aio_pika.connect(
            host=self.settings.host,
            port=self.settings.port,
            login=self.settings.user,
            password=self.settings.password,
        )

        self.channel = await self.connection.channel()
        self.exchange = await self.channel.declare_exchange(
            name=self.settings.exchange,
        )

    async def close(self) -> None:
        await self.connection.close()

    def make_routing_key(self, event: MessageType) -> str:
        return f"{self.settings.routing_prefix}{event}"
