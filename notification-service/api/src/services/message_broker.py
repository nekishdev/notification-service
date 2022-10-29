import abc

import aio_pika
from pamqp.commands import Basic

from exceptions.message_broker import MessageIsNotAckedError
from services.rmq import PikaClient
from settings import settings


class BaseMessageBroker(abc.ABC):
    @abc.abstractmethod
    async def send(self, data):
        pass


class RabbitMQMessageBroker(BaseMessageBroker):
    async def send(self, data):
        channel = await PikaClient.channel()
        routing_key = settings.RABBITMQ_QUEUE_NAME

        result = await channel.default_exchange.publish(
            aio_pika.Message(body=f"Hello {routing_key}".encode()),
            routing_key=routing_key,
        )

        if type(result) is not Basic.Ack:
            raise MessageIsNotAckedError
