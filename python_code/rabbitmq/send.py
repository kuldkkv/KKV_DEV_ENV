#!/usr/bin/env python

import pika
import sys

conn = pika.BlockingConnection(pika.ConnectionParameters('centos'))
channel = conn.channel()
channel.queue_declare(queue = 'hello')

channel.basic_publish(exchange = '',
                routing_key = 'hello',
                body = sys.argv[1])

print(" message sent")

conn.close()
