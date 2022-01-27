import pika


def callback(ch, method, properties, body):
    print(" [x] %r" % body.decode('utf-8'))


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

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='logs', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
