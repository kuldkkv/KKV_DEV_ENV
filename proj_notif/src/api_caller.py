#!/usr/bin/env python

import requests
import pprint
import psycopg2
import pandas as pd
from datetime import datetime
import pika


Q_HOST = 'centos'
Q_EXCH = 'q_consumer_notif'
Q_EXCH_TYPE = 'topic'
Q_ROUTING_KEY = 'nse_stock_data'
API_HOST = 'http://centos:5003'
API_HEADER = {'Content-Type' : 'application/json'}
DB_HOST = 'centos'
DB_NAME = 'sourcedb'
DB_USR = 'core'
DB_PASS = 'point007'


def connect_to_db():
    conn = psycopg2.connect(host = DB_HOST, dbname = DB_NAME,
                            user = DB_USR, password = DB_PASS)
    print('connected to db')
    return conn



def get_api_params_from_db(conn, source_desc):
    cur = conn.cursor()
    print('[%s]' % source_desc)

    sql = '''select eff_dt, symbol, series from core.api_param_config where source_desc = %(sd)s
        '''
    print(cur.mogrify(sql, {'sd' : source_desc}))
    cur.execute(sql, {'sd' : source_desc})
    rs = cur.fetchall()
    print('fetched [%d] rows.' % cur.rowcount)

    for r in rs:
        print(r)
    cur.close()
    return rs



def call_api(param_set):
    api_output_list = list()
    rows_df = pd.DataFrame()
    for r in param_set:
        url = API_HOST + '/service/nse_stock_data/eff_dt/' + r[0] + \
                        '/symbol/' + r[1] + \
                        '/series/' + r[2]
        print('>>> calling ', url)
        response = requests.get(url, headers = API_HEADER)
        print('*** api response code ' + str(response.status_code), end = ' ')
        #print(pprint.pprint(response.json()))
        #api_output_list.append(response.json())

        #df = pd.read_json(url)
        df = pd.DataFrame(response.json())
        #print(df)
        rows_df = rows_df.append(df)
    #return api_output_list
    return rows_df


def insert_to_db(conn, df):
    #cur = conn.cursor()

    del df['AT']
    now = datetime.now().strftime('%m%d%H%M%S')
    cols = ','.join(list(df.columns))
    tpls = [tuple(x) for x in df.to_numpy()]
    
    cols = cols + ',LOAD_ID'
    sql = 'insert into core.nse_stock_data (%s) values (%%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %s)' % (cols, now)
    print(sql)
    
    cur = conn.cursor()
    cur.executemany(sql, tpls)
    conn.commit()
    print('inserted [%d] rows.' % cur.rowcount)
    cur.close()




def api_caller_main():
    conn = connect_to_db()
    param_set = get_api_params_from_db(conn, '100')
    for r in param_set:
        print(r)
    #api_output_list = call_api(param_set)
    rows_df = call_api(param_set)

    insert_to_db(conn, rows_df)

    conn.close()

    #for r in api_output_list:
    #    print(pprint.pprint(r))



def queue_callback(ch, method, properties, body):
    data_load_status = body.decode('utf-8')
    print('data_load_statis is [%s]' % (data_load_status))
    if data_load_status == 'SUCCESS':
        api_caller_main()
    else:
        print('data load is not successfull, no loader called.')



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
