#!/usr/bin/env python

from flask import Flask, request, abort, jsonify, make_response
from flask_restful import Resource, Api
from waitress import serve
from werkzeug.exceptions import BadRequest
import datetime


app = Flask(__name__)


@app.route('/nse_stock_data/eff_dt/<v_eff_dt>/symbol/<v_symbol>/series/<v_series>', methods=['GET'])
def get_nse_stock_data(v_eff_dt, v_symbol, v_series = ''):
    print('in get function')
    print('input params are [%s] [%s] [%s]' % (v_eff_dt, v_symbol, v_series))

    # dummy return
    return { 
        'eff_dt' : v_eff_dt, 
        'symbol' : v_symbol, 
        'series' : v_series,
        'at' : datetime.datetime.now()
    }


def main():
    api = Api(app)

    print('services started ...')
    serve(app, host = '0.0.0.0', port = '5003')



if __name__ == '__main__':
    main()
