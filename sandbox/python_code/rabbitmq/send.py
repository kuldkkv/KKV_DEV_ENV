#!/usr/bin/env python

import pika
import sys

conn = pika.BlockingConnection(pika.ConnectionParameters('centos'))
channel = conn.channel()
channel.queue_declare(queue='hello', durable=True)

message = ' '.join(sys.argv[1:]) or 'Hello World!'
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=message,
                      properties=pika.BasicProperties(
                          delivery_mode=2,
                      )
                      )

print(" message sent")

conn.close()
