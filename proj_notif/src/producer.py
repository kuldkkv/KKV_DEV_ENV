#!/usr/bin/env python

import sys
import pika
import psycopg2
import os
import logging

import utils    # local lib


Q_HOST = 'centos'
Q_EXCH = 'q_producer_notif'
Q_EXCH_TYPE = 'topic'
Q_ROUTING_KEY = 'loader_start'
DB_HOST = 'centos'
DB_NAME = 'sourcedb'
DB_USR = 'core'
DB_PASS_FILE = os.environ['HOME'] + '/config/pg_sourcedb_core.enc'

STG_TABLE = 'stg.nse_stock_data'

Q_NOTIF_EXCH = 'q_consumer_notif'
Q_NOTIF_EXCH_TYPE = 'topic'
Q_NOTIF_ROUTING_KEY = 'nse_stock_data'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def queue_callback(ch, method, properties, body):
    file_name = body.decode('utf-8')
    logger.info('file name for load is [%s]' % (file_name))
    load_file(file_name)


def send_consumer_notif():
    conn = pika.BlockingConnection(pika.ConnectionParameters(Q_HOST))
    channel = conn.channel()

    channel.exchange_declare(exchange=Q_NOTIF_EXCH,
                             exchange_type=Q_NOTIF_EXCH_TYPE)
    channel.basic_publish(exchange=Q_NOTIF_EXCH,
                          routing_key=Q_NOTIF_ROUTING_KEY, body='SUCCESS')
    logger.info('notification sent.')
    conn.close()


def load_file(file_name):
    db_pass = utils.decrypt(data_file = DB_PASS_FILE)
    conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME,
                            user=DB_USR, password=db_pass)
    logger.info('connected to db')
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute('truncate table ' + STG_TABLE)
    logger.info('data truncated')

    with open(file_name, 'r') as fd:
        cur.copy_from(fd, STG_TABLE, sep=',')

    logger.info('loaded [%d] rows in stage table' % cur.rowcount)
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

    logger.info('connected to queue/topic [%s/%s]' % (Q_EXCH, Q_ROUTING_KEY))
    logger.info('waiting for messages')

    channel.basic_consume(
        queue=queue, on_message_callback=queue_callback, auto_ack=True)
    channel.start_consuming()
    conn.close()


def main():
    logger.info('-' * 40)
    logger.info('\tPRODUCER started')
    logger.info('-' * 40)
    check_for_notification()


if __name__ == '__main__':
    main()
