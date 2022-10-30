from json import dumps
from time import sleep

import pika
from models.notifications import NotificationSchema
from settings import settings

connection = pika.BlockingConnection(pika.ConnectionParameters(settings.RABBITMQ_HOST))
channel = connection.channel()

channel.queue_declare(queue=settings.RABBITMQ_QUEUE_NAME, durable=True)

data = {
    "address": "nowar1@mail.ru",
    "source": "email",
    "text": "Test message to User",
    "send_at": "2022-10-29 10:30:00",
}

dto = NotificationSchema(**data)

channel.basic_publish(
    exchange="",
    routing_key=settings.RABBITMQ_QUEUE_NAME,
    body=bytes(dumps(dto.dict(exclude_unset=True), default=str), encoding="utf-8"),
    properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE),
)

print(" [x] Sent Test message!'")

sleep(1)

connection.close()
