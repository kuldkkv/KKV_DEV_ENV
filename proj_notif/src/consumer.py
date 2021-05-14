#!/usr/bin/env python

import sys
import pika
import psycopg2


Q_HOST = 'centos'
Q_EXCH = 'q_consumer_notif'
Q_EXCH_TYPE = 'topic'
Q_ROUTING_KEY = 'nse_stock_data'
DB_HOST = 'centos'
DB_NAME = 'sourcedb'
DB_USR = 'core'
DB_PASS = '##'
STG_TABLE = 'stg.nse_stock_data'
CORE_TABLE = 'core.nse_stock_data'


def queue_callback(ch, method, properties, body):
    data_load_status = body.decode('utf-8')
    print('data_load_statis is [%s]' % (data_load_status))
    if data_load_status == 'SUCCESS':
        load_data()
    else:
        print('data load is not successfull, no loader called.')


def load_data():
    conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME,
                            user=DB_USR, password=DB_PASS)
    print('connected to db')
    conn.autocommit = True
    cur = conn.cursor()

    max_load_id_sql = '''
                SELECT COALESCE(MAX(LOAD_ID), 0) FROM CORE.NSE_STOCK_DATA;
                '''
    cur.execute(max_load_id_sql)
    max_load_id = int(cur.fetchone()[0])
    print('before max load id is, ', max_load_id)
    max_load_id += 1
    print('after max load id is, ', max_load_id)

    # load data in core table
    sql = '''
        INSERT INTO CORE.NSE_STOCK_DATA (LOAD_ID,
                SYMBOL ,
                SERIES ,
                OPEN ,
                HIGH ,
                LOW ,
                CLOSE ,
                LAST ,
                PREVCLOSE ,
                TOTTRDQTY ,
                TOTTRDVAL ,
                EFF_DT ,
                TOTALTRADES,
                ISIN)
        SELECT ''' + str(max_load_id) + ''', SYMBOL ,
                SERIES ,
                OPEN ,
                HIGH ,
                LOW ,
                CLOSE ,
                LAST ,
                PREVCLOSE ,
                TOTTRDQTY ,
                TOTTRDVAL ,
                EFF_DT ,
                TOTALTRADES,
                ISIN
        FROM STG.NSE_STOCK_DATA;
        '''
    cur.execute(sql)
    conn.commit()
    print('loaded data in core table')
    cur.close()
    conn.close()


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
