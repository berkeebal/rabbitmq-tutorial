import sys

import pika


def callback(ch, method, properties, body):
    print(f"Routing_key -> " + method.routing_key + " |||||| Message =>" + body.decode('utf-8'))


credentials = pika.PlainCredentials('user', 'password')
connection_parameters = pika.ConnectionParameters(
    'localhost',
    5672,
    '/',
    credentials
)

connection = pika.BlockingConnection(connection_parameters)
channel = connection.channel()

channel.exchange_declare(exchange='log', exchange_type='topic')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

routing_keys = sys.argv[1:]

if not routing_keys:
    print("No routing key")
    sys.exit(0)

for routing_key in routing_keys:
    channel.queue_bind(exchange='log', queue=queue_name, routing_key=routing_key)

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True
)


print(f"Listening on exchange log with routing_key/keys => {routing_keys}")
channel.start_consuming()

