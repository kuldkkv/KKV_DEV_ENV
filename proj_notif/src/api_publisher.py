#!/usr/bin/env python

from flask import Flask, request, abort, jsonify, make_response
from flask_restful import Resource, Api
from waitress import serve
from werkzeug.exceptions import BadRequest
import datetime
import psycopg2
import os
import logging

import utils    # local lib


app = Flask(__name__)

DB_HOST = 'centos'
DB_NAME = 'sourcedb'
DB_USR = 'core'
DB_PASS_FILE = os.environ['HOME'] + '/config/pg_sourcedb_core.enc'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

conn = None


def get_data_from_db(v_eff_dt, v_symbol, v_series):
    global conn

    if not conn:
        db_pass = utils.decrypt(data_file = DB_PASS_FILE)
        conn = psycopg2.connect(host = DB_HOST, dbname = DB_NAME,
                                user = DB_USR, password = db_pass)
        logger.info('connected to db')
    else:
        logger.info('reusing connection')

    cur = conn.cursor()
    sql = '''
            SELECT
                    SYMBOL,
                    SERIES,
                    OPEN,
                    HIGH,
                    LOW,
                    CLOSE,
                    LAST,
                    PREVCLOSE,
                    TOTTRDQTY,
                    TOTTRDVAL,
                    EFF_DT,
                    TOTALTRADES,
                    ISIN
            FROM
                    STG.NSE_STOCK_DATA
            WHERE
                    EFF_DT = %s
                    AND
                    SYMBOL = %s
                    AND
                    SERIES = %s;
    '''
    cur.execute(sql, (v_eff_dt, v_symbol, v_series))
    result_set = cur.fetchall()
    d = dict()
    rows_output = list()
    for row in result_set:
        d['SYMBOL'] = row[0]
        d['SERIES'] = row[1]
        d['OPEN'] = str(row[2])
        d['HIGH'] = str(row[3])
        d['LOW'] = str(row[4])
        d['CLOSE'] = str(row[5])
        d['LAST'] = str(row[6])
        d['PREVCLOSE'] = str(row[7])
        d['TOTTRDQTY'] = str(row[8])
        d['TOTTRDVAL'] = str(row[9])
        d['EFF_DT'] = row[10]
        d['TOTALTRADES'] = str(row[11])
        d['ISIN'] = row[12]
        d['AT'] = datetime.datetime.now()
        rows_output.append(d)

    cur.close()
    conn.commit()
    return rows_output


@app.route('/service/nse_stock_data/eff_dt/<v_eff_dt>/symbol/<v_symbol>/series/<v_series>', methods=['GET'])
def get_nse_stock_data(v_eff_dt, v_symbol, v_series = ''):
    logger.info('Api called, input params are [%s] [%s] [%s]' % (v_eff_dt, v_symbol, v_series))

    result_set = get_data_from_db(v_eff_dt, v_symbol, v_series)

    return jsonify(result_set), 200



def main():
    api = Api(app)

    logger.info('-' * 40)
    logger.info('\tAPI PUBLISHER Started')
    logger.info('-' * 40)
    logger.info('Api services started ...')
    serve(app, host = '0.0.0.0', port = '5003')



if __name__ == '__main__':
    main()
