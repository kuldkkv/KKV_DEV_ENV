#!/usr/bin/env python

import pika


def callback(ch, method, properties, body):
    print("Received %r" % body)


conn = pika.BlockingConnection(pika.ConnectionParameters('centos'))
channel = conn.channel()

channel.exchange_declare(exchange = 'logs', exchange_type = 'fanout')
result = channel.queue_declare(queue='', exclusive = True)
channel.queue_bind(exchange = 'logs', queue = result.method.queue)

print("waiting for message ...")

channel.basic_consume(queue=result.method.queue,
                      on_message_callback=callback, auto_ack = True)

channel.start_consuming()

conn.close()
