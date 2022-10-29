import smtplib
from email.message import EmailMessage

from models.notifications import User
from settings import settings


class EmailService:
    def send_email(self, message: EmailMessage) -> None:
        server = smtplib.SMTP_SSL(settings.EMAIL_SERVER, settings.EMAIL_PORT)
        server.login(settings.email_user, settings.email_password)

        server.sendmail(settings.email_user, [message["To"]], message.as_string())
        server.close()

    def prepare_email_message(self, user: User, title: str, text: str) -> EmailMessage:
        message = EmailMessage()
        message["From"] = settings.email_user
        message["To"] = ",".join([user.user_email])
        message["Subject"] = title

        message.add_alternative(text, subtype="html")
        return message

    def send_email_(self, user: User, title: str, text: str) -> None:
        message = self.prepare_email_message(user, title, text)
        self.send_email(message)
