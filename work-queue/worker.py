import pika
import time


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode('utf-8'))
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


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

print(' [*] Waiting for messages. To exit press CTRL+C')

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)

channel.start_consuming()
