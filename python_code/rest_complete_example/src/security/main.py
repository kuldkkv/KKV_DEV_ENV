#!/usr/bin/env python

from flask import Flask, request, abort, jsonify, make_response
from flask_restful import Resource, Api
from waitress import serve
from werkzeug.exceptions import BadRequest
from security import Security
import datetime

app = Flask(__name__)


def security_handler(dml_type):
    print('in handler function, type: ' + dml_type)
    provider_desc = None
    sub_provider_desc = None
    security_name = None
    security_type = None
    rating = None
    isin = None
    cusip = None
    cins = None
    live_cusip = None
    sedol = None
    bbc_ticker = None
    wkn = None

    current_dt = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    req_data = request.get_json()

    if dml_type == 'UPDATE' or dml_type == 'CREATE':
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

    if dml_type == 'UPDATE' or dml_type == 'DELETE':
        master_id = req_data['master_id']
    else:
        master_id = None
        

    security_obj = Security(provider_desc, sub_provider_desc,
                            security_name,
                            security_type, rating, isin, cusip, cins, live_cusip, sedol,
                            bbc_ticker, wkn, master_id)

    if dml_type == 'CREATE':
        is_valid_status = security_obj.create_security()
    elif dml_type == 'UPDATE':
        is_valid_status = security_obj.update_security()
    else:
        is_valid_status = security_obj.delete_security()

    print('security status is : ' + str(is_valid_status))

    return_message = {
        'type': security_obj.errm,
        'message': security_obj.return_message,
        'detail': security_obj.message_detail,
        'request_data': req_data,
        'system time': current_dt,
        'master_id': security_obj.master_id
    }

    print('return message is ')
    print(return_message)

    if not is_valid_status:
        print('in abort step ' + str(security_obj.errm))
        response = make_response(jsonify(message = return_message), 400)
        abort(response)
    else:
        print('passed validation step')
        print('step 5')
        return jsonify({'message': return_message}), 201


@app.route('/api/v1/createsecurity', methods=['POST'])
def create_security():
    print('in create security function')
    return security_handler('CREATE')
    

@app.route('/api/v1/updatesecurity', methods=['PUT'])
def update_security():
    print('in update security function')
    return security_handler('UPDATE')
    

@app.route('/api/v1/deletesecurity', methods=['DELETE'])
def delete_security():
    print('in delete security function')
    return security_handler('DELETE')
    


def main():
    api = Api(app)

    #app.run(host = '0.0.0.0', port = '5002')
    serve(app, host='0.0.0.0', port='5003')


if __name__ == '__main__':
    main()
