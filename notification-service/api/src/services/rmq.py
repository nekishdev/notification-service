import aio_pika
from aio_pika.abc import AbstractRobustConnection, AbstractRobustChannel

from settings import settings


class PikaClient(object):
    """
    Синглтон для единственного подключения к RabbitMQ.
    """

    __connection: AbstractRobustConnection = None
    __channel: AbstractRobustChannel = None

    @classmethod
    async def get_connection(cls) -> AbstractRobustConnection:
        if not cls.__connection:
            cls.__connection = await aio_pika.connect_robust(
                f"amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASSWORD}@{settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}/",
            )
        return cls.__connection

    @classmethod
    async def channel(cls) -> AbstractRobustChannel:
        if not cls.__channel:
            conn = await cls.get_connection()
            cls.__channel = await conn.channel()
            await cls.__channel.declare_queue(
                settings.RABBITMQ_QUEUE_NAME, durable=True
            )

        return cls.__channel
