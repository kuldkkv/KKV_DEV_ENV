#!/usr/bin/env python

from flask import Flask, request, abort, jsonify, make_response
from flask_restful import Resource, Api
from waitress import serve
from werkzeug.exceptions import BadRequest
from security import Security
import datetime

app = Flask(__name__)


@app.route('/api/v1/createsecurity', methods=['POST'])
def create_security():
    print('in create security function')

    current_dt = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    req_data = request.get_json()
    provider_desc = req_data['provider_desc']
    sub_provider_desc = req_data['sub_provider_desc']
    security_name = req_data['security_name']
    security_type = req_data['security_type']
    rating = req_data['rating']
    isin = req_data['isin']
    cusip = req_data['cusip']
    cins = req_data['cins']
    live_cusip = req_data['live_cusip']
    sedol = req_data['sedol']
    bbc_ticker = req_data['bbc_ticker']
    wkn = req_data['wkn']

    security_obj = Security(provider_desc, sub_provider_desc,
                            security_name,
                            security_type, rating, isin, cusip, cins, live_cusip, sedol,
                            bbc_ticker, wkn)

    is_valid_status = security_obj.create_security()
    print('In main : ' + str(is_valid_status))

    if not is_valid_status:
        print('in abort step ' + str(security_obj.errm))
        e1 = {
            'type': security_obj.errm,
            'message': 'Security creation failed',
            'detail': 'New security creation failed at attribute validation step',
            'request_data': req_data,
            'system time': current_dt
        }
        response = make_response(jsonify(message=e1), 400)
        abort(response)
    else:
        print('passed validation step')
        return_message = {
            'message': 'New secuity sucessfully created',
            'master_id': security_obj.master_id
        }
        print('step 5')
        return jsonify({'message': return_message}), 201


def main():
    api = Api(app)

    #app.run(host = '0.0.0.0', port = '5002')
    serve(app, host='0.0.0.0', port='5003')


if __name__ == '__main__':
    main()
