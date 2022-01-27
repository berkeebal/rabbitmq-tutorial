import pika
import sys

credentials = pika.PlainCredentials('user', 'password')
connection_parameters = pika.ConnectionParameters(
    'localhost',
    5672,
    '/',
    credentials
)

connection = pika.BlockingConnection(connection_parameters)
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(
    exchange='',
    routing_key='task_queue',
    body=message.encode(encoding='utf-8'),
    properties=pika.BasicProperties(
        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
    )
)
print(" [x] Sent %r" % message)
connection.close()
