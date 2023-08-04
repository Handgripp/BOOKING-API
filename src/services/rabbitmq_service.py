import pika


class RabbitMQ:
    def __init__(self, config=None):
        self.config = config
        if config is not None:
            self.init_app(config)

    def init_app(self, config):
        self.host = config['host']
        self.port = config['port']
        self.user = config['user']
        self.password = config['password']
        self.queue_name = config['queue_name']

    def send_message(self, message):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host, port=self.port,
                                      credentials=pika.PlainCredentials(self.user, self.password))
        )
        channel = connection.channel()
        channel.queue_declare(queue=self.queue_name)
        channel.basic_publish(exchange='', routing_key=self.queue_name, body=message)
        connection.close()

    def consume_messages(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host, port=self.port,
                                      credentials=pika.PlainCredentials(self.user, self.password))
        )
        channel = connection.channel()
        channel.queue_declare(queue=self.queue_name)

        for method_frame, properties, body in channel.consume(self.queue_name):
            yield body.decode()
            channel.basic_ack(method_frame.delivery_tag)

        connection.close()
