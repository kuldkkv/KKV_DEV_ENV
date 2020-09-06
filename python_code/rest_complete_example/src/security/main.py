#!/usr/bin/env python

from flask import Flask, request, abort, jsonify, make_response
from flask_restful import Resource, Api
from waitress import serve
from werkzeug.exceptions import BadRequest
import psycopg2
import datetime

app = Flask(__name__)
conn = None

def get_new_master_id():
    global conn
    conn = psycopg2.connect(host="openbsd.64",database="pgdb1", user="kkv1", password="point007")

    cur = conn.cursor()
    cur.execute("select nextval('securitydbo.master_id_seq')")
    master_id = cur.fetchone()[0]
    cur.close()
    return master_id


def create_security_rec_in_db(master_id, provider_desc, sub_provider_desc, security_name,
        security_type, rating, isin, cusip, cins, live_cusip, sedol, bbc_ticker,
        wkn):
    current_tm = datetime.datetime.now()
    cur = conn.cursor()
    data = [master_id, provider_desc, sub_provider_desc, security_name,
            security_type, rating, isin, cusip, cins, live_cusip, sedol, bbc_ticker,
            wkn, current_tm, current_tm]
    cur.execute('''Insert into securitydbo.master (
                    master_id,
                    provider_desc,
                    sub_provider_desc,
                    security_name,
                    security_type,
                    rating,
                    isin,
                    cusip,
                    cins,
                    live_cusip,
                    sedol,
                    bbc_ticker,
                    wkn,
                    insert_ts,
                    update_ts)
                Values (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s)''',
            data)
    conn.commit()
    print('data inserted')
    cur.close()
    conn.close()

    

def valid_security_request(provider_desc, sub_provider_desc, security_name,
            security_type, rating, isin, cusip, cins, live_cusip, sedol, 
            bbc_ticker, wkn):
    if not provider_desc or not sub_provider_desc or not security_name or not security_type:
        return False, "ERROR_MANDATORY_FIELDS"
    if not (isin or cusip or cins or live_cusip or sedol or bbc_ticker or wkn):
        return False, "ERROR_NO_XREF"
    return True, None


@app.route('/api/v1/createsecurity', methods = ['POST'])
def create_security():
    print('in create security function')

    current_dt = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    req_data = request.get_json()
    provider_desc= req_data['provider_desc']
    sub_provider_desc=req_data['sub_provider_desc']
    security_name=req_data['security_name']
    security_type=req_data['security_type']
    rating=req_data['rating']
    isin=req_data['isin']
    cusip=req_data['cusip']
    cins=req_data['cins']
    live_cusip=req_data['live_cusip']
    sedol=req_data['sedol']
    bbc_ticker=req_data['bbc_ticker']
    wkn=req_data['wkn']

    is_valid_status, err_mesg = valid_security_request(provider_desc, sub_provider_desc, 
            security_name,
            security_type, rating, isin, cusip, cins, live_cusip, sedol, 
            bbc_ticker, wkn)

    if not is_valid_status:
        print('in abort step ' + err_mesg)
        e1 = {
            'type' : err_mesg,
            'message' : 'Security creation failed',
            'detail' : 'New security creation failed at attribute validation step',
            'request_data' : req_data,
            'system time' : current_dt
        }
        response = make_response(jsonify(message = e1), 400)
        abort(response)
    print('passed validation step')

    master_id = get_new_master_id();

    create_security_rec_in_db(master_id, provider_desc, sub_provider_desc, security_name,
        security_type, rating, isin, cusip, cins, live_cusip, sedol, bbc_ticker,
        wkn)
    
    return_message = {
        'message' : 'New secuity sucessfully created',
        'master_id' : master_id
    }
    print('step 5')
    return jsonify({'message' : return_message}), 201


def main():
    api = Api(app)

    #app.run(host = '0.0.0.0', port = '5002')
    serve(app, host = '0.0.0.0', port = '5003')



if __name__ == '__main__':
    main()

