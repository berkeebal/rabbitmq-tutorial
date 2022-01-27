import os
import pika
import sys


def main():

	credentials = pika.PlainCredentials('user', 'password')
	connection_parameters = pika.ConnectionParameters(
		'localhost',
		5672,
		'/'
		'',
		credentials
	)
	connection = pika.BlockingConnection(connection_parameters)
	channel = connection.channel()
	channel.queue_declare(queue='hello')
	
	def callback(ch, method, properties, body):
		print(f'{body}')
	
	channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)
	print("consumers starts listening ctrl+c to abort")
	channel.start_consuming()


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print('Interrupted')
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)

