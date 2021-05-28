#!/usr/bin/env python

import requests
import psycopg2
import pandas as pd
from datetime import datetime
import pika
import os
import logging

import utils    # local lib


Q_HOST = 'centos'
Q_EXCH = 'q_consumer_notif'
Q_EXCH_TYPE = 'topic'
Q_ROUTING_KEY = 'nse_stock_data'
API_HOST = 'http://centos:5003'
API_HEADER = {'Content-Type' : 'application/json'}
DB_HOST = 'centos'
DB_NAME = 'sourcedb'
DB_USR = 'core'
DB_PASS_FILE = os.environ['HOME'] + '/config/pg_sourcedb_core.enc'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def connect_to_db():
    db_pass = utils.decrypt(data_file = DB_PASS_FILE)
    conn = psycopg2.connect(host = DB_HOST, dbname = DB_NAME,
                            user = DB_USR, password = db_pass)
    logger.info('connected to db')
    return conn



def get_api_params_from_db(conn, source_desc):
    cur = conn.cursor()
    logger.info('fetching api params for source [%s]' % source_desc)

    sql = '''select eff_dt, symbol, series from core.api_param_config where source_desc = %(sd)s
        '''
    logger.debug(cur.mogrify(sql, {'sd' : source_desc}))
    cur.execute(sql, {'sd' : source_desc})
    rs = cur.fetchall()
    logger.info('fetched [%d] rows.' % cur.rowcount)

    for r in rs:
        logger.debug(r)
    cur.close()
    return rs



def call_api(param_set):
    api_output_list = list()
    rows_df = pd.DataFrame()
    for r in param_set:
        url = API_HOST + '/service/nse_stock_data/eff_dt/' + r[0] + \
                        '/symbol/' + r[1] + \
                        '/series/' + r[2]
        logger.info('calling api [%s]' % url)
        response = requests.get(url, headers = API_HEADER)
        logger.info('api response code ' + str(response.status_code))
        df = pd.DataFrame(response.json())
        rows_df = rows_df.append(df)
    return rows_df


def insert_to_db(conn, df):
    #cur = conn.cursor()

    del df['AT']
    now = datetime.now().strftime('%m%d%H%M%S')
    cols = ','.join(list(df.columns))
    tpls = [tuple(x) for x in df.to_numpy()]
    
    cols = cols + ',LOAD_ID'
    sql = 'insert into core.nse_stock_data (%s) values (%%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %s)' % (cols, now)
    logger.debug(sql)
    
    cur = conn.cursor()
    logger.info('inserting data to db ...')
    cur.executemany(sql, tpls)
    conn.commit()
    logger.info('inserted [%d] rows.' % cur.rowcount)
    cur.close()




def api_caller_main():
    conn = connect_to_db()

    param_set = get_api_params_from_db(conn, '100')
    rows_df = call_api(param_set)
    insert_to_db(conn, rows_df)

    conn.close()



def queue_callback(ch, method, properties, body):
    data_load_status = body.decode('utf-8')
    logger.info('data_load_status is [%s]' % (data_load_status))
    if data_load_status == 'SUCCESS':
        api_caller_main()
    else:
        logger.warning('data load is not successful, no loader called.')



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
    logger.info('\tCONSUMER started')
    logger.info('-' * 40)
    check_for_notification()


if __name__ == '__main__':
    main()
