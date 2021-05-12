#!/usr/bin/env python

import pika
import sys

conn = pika.BlockingConnection(pika.ConnectionParameters('centos'))
channel = conn.channel()

channel.exchange_declare(exchange = 'logs', exchange_type = 'fanout')

message = ' '.join(sys.argv[1:]) or 'Hello World!'

channel.basic_publish(exchange='logs',
                      routing_key='',
                      body=message
                      )

print("message sent", message)

conn.close()
