from models.notifications import User
from services.mail_sender import AbstractSender


class EmailService:
    def __init__(self, mail_sender: AbstractSender) -> None:
        self.mail_sender = mail_sender

    def send_email(self, user: User, subject: str, text: str) -> None:
        self.mail_sender.send(user, subject, text)


class TelegramService:
    def __init__(self) -> None:
        pass

    def send_email(self, user: User, subject: str, text: str) -> None:
        pass
