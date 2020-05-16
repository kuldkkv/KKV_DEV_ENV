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


def call_post_api(api_endpoint, payload):
    print("===== calling API {:s} =====".format(api_endpoint))
    print(pprint.pprint(payload))
    resp = requests.post(api_endpoint, json=payload)
    print("API status code {:d}".format(resp.status_code))

    if resp.status_code != 201:
        raise Exception('API POST Error /task {}'.format(resp.status_code))

