"""
Message Acknowledgement

If a worker dies before finishing a task,
task will be undone and lost. To prevent this unwanted
behaviour RabbitMQ uses message acknowledgement and marks
task in queue's as finished if not the task will be send to
another work queue when its possible.
EX:
  def callback(ch, method, properties, body):
    ...
    ch.basic_ack(delivery_tag=method.delivery_tag)

Also mark queues as durable with 'durable=True' flag
to losing a task if the rabbitmq server downs.

TO send the messages in durable way publish them like this:

channel.basic_publish(
    exchange=''
    body=message,
    routing_key='queue_name'
    properties=pike.BasicProperties(
        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
    )
)

To fair dispatch messages to workers use:
    channel.basic_qos(prefetch_count=1)
"""