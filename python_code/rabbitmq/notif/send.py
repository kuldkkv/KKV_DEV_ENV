#!/usr/bin/env python

import pika
import sys
import datetime

conn = pika.BlockingConnection(pika.ConnectionParameters('centos'))
channel = conn.channel()

channel.exchange_declare(exchange = 'fa_notif', exchange_type = 'direct')

#message = ' '.join(sys.argv[1:]) or 'Hello World!'

entity = sys.argv[1] if len(sys.argv) > 1 else '<ERROR>'

message = entity + ' ready at ' + str(datetime.datetime.now())

channel.basic_publish(exchange='fa_notif',
                      routing_key=entity,
                      body=message
                      )

print("message %r sent for %r" % (message, entity))

conn.close()
