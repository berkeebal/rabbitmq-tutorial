import sys

import pika


credentials = pika.PlainCredentials('user', 'password')
parameters = pika.ConnectionParameters(
    'localhost',
    5672,
    '/',
    credentials
)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.exchange_declare(exchange='log', exchange_type='topic')

routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
message = " ".join(sys.argv[2:]) or "Hello World!"

channel.basic_publish(exchange='log', routing_key=routing_key, body=message.encode('utf-8'))
connection.close()
