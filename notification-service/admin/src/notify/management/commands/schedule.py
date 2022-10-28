import datetime
from time import sleep

import requests

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from notify.models import Message, MessagesStatusChoices


class Command(BaseCommand):
    help = "Send scheduled notifications"

    def handle(self, *args, **options):
        while True:
            try:
                self.__process_waiting_message()
            except Exception as e:
                self.stdout.info(e)

            sleep(20)

    def __process_waiting_message(self):
        messages: list[Message] = Message.objects.filter(
            status=MessagesStatusChoices.WAIT, send_at__lte=datetime.datetime.now()
        )

        for message in messages:
            self.__send_to_api(message)

    def __send_to_api(self, message: Message):
        data = {
            "id": str(message.id),
            "address": message.address,
            "source": message.source,
            "text": message.text,
            "send_at": str(message.send_at),
        }
        r = requests.post(
            f"{settings.NOTIFICATION_API_BASE_URL}/api/v1/notify/send", json=data
        )
        if r.status_code != 200:
            raise Exception(
                f"Failed response from Notification API [status: {r.status_code}]. {r.content}"
            )
