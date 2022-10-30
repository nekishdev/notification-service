from abc import ABC, abstractmethod

from email.message import EmailMessage
from settings import settings
from models.notifications import User
import smtplib


class AbstractSender(ABC):
    @abstractmethod
    def send(self, user: User, subject: str, text: str):
        pass


class MailHogSender(AbstractSender):
    def send_email(self, message: EmailMessage) -> None:
        server = smtplib.SMTP(settings.MAILHOG_HOST, settings.MAILHOG_PORT)
        server.sendmail(settings.EMAIL_USER, [message["To"]], message.as_string())
        server.close()

    def prepare_email_message(self, user: User, subject: str, text: str) -> EmailMessage:
        message = EmailMessage()
        message["From"] = settings.EMAIL_USER
        message["To"] = ",".join([user.user_email])
        message["Subject"] = subject

        message.add_alternative(text, subtype="html")
        return message

    def send(self, user: User, subject: str, text: str):
        message = self.prepare_email_message(user, subject, text)
        self.send_email(message)


class MailSender(AbstractSender):
    def send_email(self, message: EmailMessage) -> None:
        server = smtplib.SMTP_SSL(settings.EMAIL_SERVER, settings.EMAIL_PORT)
        server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)

        server.sendmail(settings.EMAIL_USER, [message["To"]], message.as_string())
        server.close()

    def prepare_email_message(self, user: User, subject: str, text: str) -> EmailMessage:
        message = EmailMessage()
        message["From"] = settings.EMAIL_USER
        message["To"] = ",".join([user.user_email])
        message["Subject"] = subject

        message.add_alternative(text, subtype="html")
        return message

    def send(self, user: User, subject: str, text: str):
        message = self.prepare_email_message(user, subject, text)
        self.send_email(message)
