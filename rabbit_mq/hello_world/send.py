#!/usr/bin/env python
import pika
import datetime


conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = conn.channel()

channel.queue_declare(queue = 'hello')

datetime_object = datetime.datetime.now()
print(datetime_object)

channel.basic_publish(exchange = '',
                        routing_key = 'hello',
                        body = 'Hello World! @ ' + str(datetime_object))

print('sent hello world')

conn.close()
