#!/usr/bin/env python

import pika


def callback(ch, method, properties, body):
    print("Received %r" % body)
    ch.basic_ack(delivery_tag=method.delivery_tag)


conn = pika.BlockingConnection(pika.ConnectionParameters('centos'))
channel = conn.channel()
channel.queue_declare(queue='hello', durable=True)
print("waiting for message ...")

channel.basic_consume(queue='hello',
                      on_message_callback=callback)

channel.start_consuming()

conn.close()
