import asyncio
from datetime import datetime, timezone
from json import loads
from uuid import uuid4

import pytz
from aio_pika import connect
from aio_pika.abc import AbstractIncomingMessage
from services.worker_service import save_message, set_message_status
from logger import app_logger
from models.notifications import Message, NotificationSchema, User
from services.notification_service import EmailService
from settings import dsl, pg_settings, settings
from services.mail_sender import MailHogSender, MailSender


async def on_message(message: AbstractIncomingMessage) -> None:
    """
    Processing messages (emails)
    """
    if message.body is not None:
        msg = loads(message.body or "")
        ns = NotificationSchema(**msg)

        user = User(username="", user_email=ns.address)
        title = ns.subject or ""
        text = ns.text
        if ns.source == "email":
            utc = pytz.UTC
            dt = datetime.now(timezone.utc)

            try:
                id = ns.id if ns.id else uuid4()

                msg = Message(
                    id=id,
                    created=dt,
                    modified=dt,
                    address=ns.address,
                    source=ns.source,
                    subject=title,
                    text=ns.text,
                    send_at=ns.send_at,
                    status="processing",
                )
                save_message(msg)

                if ns.send_at is None or utc.localize(ns.send_at) <= dt:
                    if settings.TESTING:
                        email_service = EmailService(mail_sender=MailHogSender())
                    else:
                        email_service = EmailService(mail_sender=MailSender())
                    email_service.send_email(user, title, text)

                    msg.status = "success"
                    msg.modified = datetime.now(timezone.utc)

                    set_message_status(msg)
            except Exception as e:
                msg.status = "failed"
                set_message_status(msg)
                app_logger.error("process msg: {message}".format(message=e))


async def main() -> None:
    # Perform connection
    connection = await connect(
        f"amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASSWORD}@{settings.RABBITMQ_HOST}/"
    )
    async with connection:
        # Creating a channel
        channel = await connection.channel()

        # Declaring queue
        queue = await channel.declare_queue(settings.RABBITMQ_QUEUE_NAME, durable=True)

        # Start listening the queue
        await queue.consume(on_message, no_ack=True)

        print(" [*] Waiting for messages. To exit press CTRL+C")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
