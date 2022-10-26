from fastapi import APIRouter, Depends

import api.v1.schemas.notification as schemas
import providers
import services.notification_service as notification_service
from api.v1 import messages
from dto.notification import NotificationDTO
from services.message_broker import BaseMessageBroker

router = APIRouter()


@router.post(
    "/send",
    response_model=schemas.NotificationSendResponseSchema,
    summary=messages.handler_send_summary,
)
async def send(
    data: schemas.NotificationSendRequestSchema,
    message_broker: BaseMessageBroker = Depends(providers.get_message_broker),
):
    dto = NotificationDTO(
        id=data.id,
        address=data.address,
        source=data.source,
        text=data.text,
        send_at=data.send_at,
    )
    await notification_service.send(dto, message_broker)
    return schemas.NotificationSendResponseSchema()
