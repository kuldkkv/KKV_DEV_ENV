#!/usr/bin/env python

import requests
import pprint
import psycopg2
import pandas as pd


API_HOST = 'http://centos:5003'
API_HEADER = {'Content-Type' : 'application/json'}
DB_HOST = 'centos'
DB_NAME = 'sourcedb'
DB_USR = 'core'
DB_PASS = 'point007'


def get_api_params_from_db(source_desc):
    conn = psycopg2.connect(host = DB_HOST, dbname = DB_NAME,
                            user = DB_USR, password = DB_PASS)
    print('connected to db')
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
    conn.close()
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
        print('*** api response code ' + str(response.status_code))
        print("*** headers:"+ str(response.headers))
        print("*** api output:")
        #print(pprint.pprint(response.json()))
        #api_output_list.append(response.json())

        #df = pd.read_json(url)
        df = pd.DataFrame(response.json())
        #print(df)
        rows_df = rows_df.append(df)
    #return api_output_list
    return rows_df



def main():
    param_set = get_api_params_from_db('N1')
    for r in param_set:
        print(r)
    #api_output_list = call_api(param_set)
    rows_df = call_api(param_set)

    print(rows_df)

    #for r in api_output_list:
    #    print(pprint.pprint(r))



if __name__ == '__main__':
    main()
