import json
from src.services.rabbitmq_service import RabbitMQ
from src.services.email_service import send_mail


def mail_consumer(config, queue):
    rabbitmq = RabbitMQ(config)
    for message in rabbitmq.consume_messages():
        queue.put(message)
        parsed_message = json.loads(message)
        send_mail(parsed_message['email'], parsed_message['subject'], parsed_message['body'])

