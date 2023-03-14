from pydantic import BaseSettings


class RabbitMQSettings(BaseSettings):
    host: str = "localhost"
    port: int = 5672
    user: str = "user"
    password: str = "password"
    exchange: str = "betting"
    routing_prefix: str = "betting."

    class Config:
        env_prefix = "RABBITMQ_"
