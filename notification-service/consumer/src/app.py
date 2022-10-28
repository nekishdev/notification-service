import pika
import sys
import os

from settings import settings

from services.notification_service import EmailService
from json import loads

from models.notifications import NotificationSchema, User


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST))
    channel = connection.channel()

    channel.queue_declare(queue=settings.RABBITMQ_QUEUE_NAME, durable=True)

    email_service = EmailService()

    def send_notification_callback(ch, method, properties, body):
        try:
            if body is not None:
                message = loads(body or '')
                ns = NotificationSchema(**message)

                user = User(username='', user_email=ns.address)
                title = ns.title or ''
                text = ns.text
                if ns.source == 'email':
                    email_service.send_email_(user, title, text)

        except Exception as e:
            print('Error: ' + str(e))

        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue=settings.RABBITMQ_QUEUE_NAME, on_message_callback=send_notification_callback, auto_ack=False)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


# def main():
#     connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST))
#     channel = connection.channel()
#
#     channel.queue_declare(queue=settings.RABBITMQ_QUEUE_NAME, durable=True)
#
#     email_service = EmailService()
#
#     def send_email_callback(ch, method, properties, body):
#         print(" [x] Received %r" % body)
#
#         try:
#             message = loads(body or '')
#             username = message['first_name'] + ' ' + message['last_name']
#             email = message['email']
#             user = User(username=username, user_email=email)
#
#             confirm_link = 'https://3logic.ru/'
#
#             email_service.send_email_confirmation(user, confirm_link=confirm_link)
#             print(" [x] Send email to %r" % username)
#         except Exception as e:
#             print('Error: ' + str(e))
#
#         ch.basic_ack(delivery_tag=method.delivery_tag)
#
#     channel.basic_consume(queue=settings.RABBITMQ_QUEUE_NAME, on_message_callback=send_email_callback, auto_ack=False)
#
#     print(' [*] Waiting for messages. To exit press CTRL+C')
#     channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
