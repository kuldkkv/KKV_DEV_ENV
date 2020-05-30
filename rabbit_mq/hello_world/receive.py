#!/usr/bin/env python
import pika


def callback(ch, method, properties, body):
    print("received %r" % body)


conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = conn.channel()

channel.queue_declare(queue = 'hello')

channel.basic_consume(queue = 'hello',
                        auto_ack = True,
                        on_message_callback = callback)

print ('waiting for messages')
channel.start_consuming()

