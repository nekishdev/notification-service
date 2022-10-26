from dto.notification import NotificationDTO
from services.message_broker import BaseMessageBroker


async def send(data: NotificationDTO, message_broker: BaseMessageBroker):
    await message_broker.send(data.dict())
