#!/usr/bin/env python

from flask import Flask, request, abort, jsonify, make_response
from flask_restful import Resource, Api
from waitress import serve
from werkzeug.exceptions import BadRequest
from security import Security
import datetime

app = Flask(__name__)


def security_handler(op_type):
    print('in handler function, type: ' + op_type)

    current_dt = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    json_data = request.get_json()

    security_obj = Security(
                        json_data.get('provider_desc'),
                        json_data.get('sub_provider_desc'),
                        json_data.get('security_name'),
                        json_data.get('security_type'),
                        json_data.get('rating'),
                        json_data.get('isin'),
                        json_data.get('cusip'),
                        json_data.get('cins'),
                        json_data.get('live_cusip'),
                        json_data.get('sedol'),
                        json_data.get('bbc_ticker'),
                        json_data.get('wkn'),
                        json_data.get('master_id'),
                        op_type
                    )

    is_valid_status = security_obj.serve()

    print('security status is : ' + str(is_valid_status))

    return_message = {
        'type': security_obj.errm,
        'message': security_obj.return_message,
        'detail': security_obj.message_detail,
        'request_data': json_data,
        'system time': current_dt,
        'master_id': security_obj.master_id
    }

    if op_type == 'GET':
        return_message['security_data'] = security_obj.security_ref_json

    print('return message is ')
    print(return_message)

    if not is_valid_status:
        print('in abort step ' + str(security_obj.errm))
        response = make_response(jsonify(message = return_message), 400)
        abort(response)
    else:
        print('passed validation step')
        return jsonify({'message': return_message}), 201


@app.route('/api/v1/createsecurity', methods=['POST'])
def create_security():
    print('in create security function')
    return security_handler('POST')
    

@app.route('/api/v1/updatesecurity', methods=['PUT'])
def update_security():
    print('in update security function')
    return security_handler('PUT')
    

@app.route('/api/v1/deletesecurity', methods=['DELETE'])
def delete_security():
    print('in delete security function')
    return security_handler('DELETE')
    

@app.route('/api/v1/security', methods=['GET'])
def get_security():
    print('in get security function')
    return security_handler('GET')
    


def main():
    api = Api(app)

    #app.run(host = '0.0.0.0', port = '5002')
    serve(app, host='0.0.0.0', port='5003')


if __name__ == '__main__':
    main()
