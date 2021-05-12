#!/usr/bin/env python

import pika
import sys


def callback(ch, method, properties, body):
    print("Received %r" % body)


conn = pika.BlockingConnection(pika.ConnectionParameters('centos'))
channel = conn.channel()

channel.exchange_declare(exchange = 'fa_notif', exchange_type = 'direct')
result = channel.queue_declare(queue='', exclusive = True)

channel.queue_bind(exchange = 'fa_notif', queue = result.method.queue,
                    routing_key = 'HOLDING')
channel.queue_bind(exchange = 'fa_notif', queue = result.method.queue,
                    routing_key = 'TRAN')

print("waiting for message from all ...")

channel.basic_consume(queue=result.method.queue,
                      on_message_callback=callback, auto_ack = True)

channel.start_consuming()

conn.close()
