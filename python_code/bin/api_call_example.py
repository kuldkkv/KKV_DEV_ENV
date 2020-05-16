#!/usr/bin/env python

import requests
import sys
import pprint

def call_get_api(api_endpoint):
    print("===== calling API {:s} =====".format(api_endpoint))
    resp = requests.get(api_endpoint)
    print("API status code {:d}".format(resp.status_code))

    if resp.status_code != 200:
        raise Exception('API GET Error /task {}'.format(resp.status_code))

    print(pprint.pprint(resp.json()))

if len(sys.argv) < 2:
    print("usage: {:s} <api endpoint>".format(sys.argv[0]))
    exit(1)

for endpoint in sys.argv[1:]:
    try:
        call_get_api(endpoint)
    except Exception as e:
        print(e)
