from services.message_broker import BaseMessageBroker, RabbitMQMessageBroker


async def get_message_broker() -> BaseMessageBroker:
    return RabbitMQMessageBroker()
