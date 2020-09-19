#!/usr/bin/env python

import requests
import sys
import pprint

api_server = 'http://openbsd.64:5003'
api_header = {"Content-Type": "application/json"}


def get_api_caller(endpoint, data):
    url = api_server + '/api/v1/security'
    response = requests.get(url, headers = api_header, data = data)

    print('*** api response code ' + str(response.status_code))
    print("*** headers:"+ str(response.headers))
    print("*** api output:")
    print(pprint.pprint(response.json()))


def post_api_caller(endpoint, data):
    url = api_server + '/api/v1/createsecurity'
    response = requests.post(url, headers = api_header, data = data)

    print('*** api response code ' + str(response.status_code))
    print("*** headers:"+ str(response.headers))
    print("*** api output:")
    print(pprint.pprint(response.json()))


def put_api_caller(endpoint, data):
    url = api_server + '/api/v1/updatesecurity'
    response = requests.put(url, headers = api_header, data = data)

    print('*** api response code ' + str(response.status_code))
    print("*** headers:"+ str(response.headers))
    print("*** api output:")
    print(pprint.pprint(response.json()))


def del_api_caller(endpoint, data):
    url = api_server + '/api/v1/deletesecurity'
    response = requests.delete(url, headers = api_header, data = data)

    print('*** api response code ' + str(response.status_code))
    print("*** headers:"+ str(response.headers))
    print("*** api output:")
    print(pprint.pprint(response.json()))



def main():
    if len(sys.argv) < 3:
        print('usage: api_consumer <endpoint> <payload>')
        sys.exit(1)
    if sys.argv[1] == 'GET':
        get_api_caller(sys.argv[1], sys.argv[2])
    elif sys.argv[1] == 'POST':
        post_api_caller(sys.argv[1], sys.argv[2])
    elif sys.argv[1] == 'PUT':
        put_api_caller(sys.argv[1], sys.argv[2])
    elif sys.argv[1] == 'DELETE':
        del_api_caller(sys.argv[1], sys.argv[2])
    else:
        raise Exception('unknown endpoint')


if __name__ == '__main__':
    sys.exit(main())
