#!/usr/bin/env python

import pika
import sys


def callback(ch, method, properties, body):
    print("Received %r" % body)


conn = pika.BlockingConnection(pika.ConnectionParameters('centos'))
channel = conn.channel()

channel.exchange_declare(exchange = 'fa_notif_topic', exchange_type = 'topic')
result = channel.queue_declare(queue='', exclusive = True)

channel.queue_bind(exchange = 'fa_notif_topic', queue = result.method.queue,
                    routing_key = sys.argv[1])

print("waiting for message from %r ..." % sys.argv[1])

channel.basic_consume(queue=result.method.queue,
                      on_message_callback=callback, auto_ack = True)

channel.start_consuming()

conn.close()
