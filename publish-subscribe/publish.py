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

channel.exchange_declare(exchange='logs', exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or "info: Hello World!"
channel.basic_publish(exchange='logs', routing_key='', body=message.encode('utf-8'))
print(" [x] Sent %r" % message)
connection.close()
