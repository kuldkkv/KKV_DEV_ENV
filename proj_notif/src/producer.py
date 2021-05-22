#!/usr/bin/env python

import sys
import pika
import psycopg2


Q_HOST = 'centos'
Q_EXCH = 'q_producer_notif'
Q_EXCH_TYPE = 'topic'
Q_ROUTING_KEY = 'loader_start'
DB_HOST = 'centos'
DB_NAME = 'sourcedb'
DB_USR = 'core'
DB_PASS = 'point007'
STG_TABLE = 'stg.nse_stock_data'

Q_NOTIF_EXCH = 'q_consumer_notif'
Q_NOTIF_EXCH_TYPE = 'topic'
Q_NOTIF_ROUTING_KEY = 'nse_stock_data'


def queue_callback(ch, method, properties, body):
    file_name = body.decode('utf-8')
    print('file name for load is [%s]' % (file_name))
    load_file(file_name)


def send_consumer_notif():
    conn = pika.BlockingConnection(pika.ConnectionParameters(Q_HOST))
    channel = conn.channel()

    channel.exchange_declare(exchange=Q_NOTIF_EXCH,
                             exchange_type=Q_NOTIF_EXCH_TYPE)
    channel.basic_publish(exchange=Q_NOTIF_EXCH,
                          routing_key=Q_NOTIF_ROUTING_KEY, body='SUCCESS')
    print('notification sent.')
    conn.close()


def load_file(file_name):
    conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME,
                            user=DB_USR, password=DB_PASS)
    print('connected to db')
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute('truncate table ' + STG_TABLE)
    print('data truncated')

    with open(file_name, 'r') as fd:
        cur.copy_from(fd, STG_TABLE, sep=',')

    print('stage data loaded')
    conn.commit()
    cur.close()
    conn.close()

    send_consumer_notif()


def check_for_notification():
    conn = pika.BlockingConnection(pika.ConnectionParameters(Q_HOST))
    channel = conn.channel()

    channel.exchange_declare(exchange=Q_EXCH, exchange_type=Q_EXCH_TYPE)
    result = channel.queue_declare(queue='', exclusive=True)
    queue = result.method.queue
    channel.queue_bind(exchange=Q_EXCH, queue=queue, routing_key=Q_ROUTING_KEY)

    print('connected to queue/topic [%s/%s]' % (Q_EXCH, Q_ROUTING_KEY))
    print('waiting for messages')

    channel.basic_consume(
        queue=queue, on_message_callback=queue_callback, auto_ack=True)
    channel.start_consuming()
    conn.close()


def main():
    check_for_notification()


if __name__ == '__main__':
    main()
