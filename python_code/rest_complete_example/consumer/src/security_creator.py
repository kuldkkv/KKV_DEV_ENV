#!/usr/bin/env python

import pandas as pd
import requests
import sys
import pprint
import datetime

api_server = 'http://openbsd.64:5003'
api_header = {"Content-Type": "application/json"}



def post_api_caller(data):
    url = api_server + '/api/v1/createsecurity'
    response = requests.post(url, headers = api_header, data = data)

    print('*** api response code ' + str(response.status_code))
    print("*** headers:"+ str(response.headers))
    print("*** api output:")
    print(pprint.pprint(response.json()))



def main():
    if len(sys.argv) < 3:
        print('usage: security_creator <provider> <subprovider>')
        sys.exit(1)
    provider_desc = sys.argv[1]
    sub_provider_desc = sys.argv[2]
    df = pd.read_csv('security_data.csv')
    df['provider_desc'] =  df['provider_desc'] + '_' + provider_desc
    df['sub_provider_desc'] =  df['sub_provider_desc'] + '_' + sub_provider_desc
    print('data loaded')

    for i in range(len(df)):
        print(datetime.datetime.now(), provider_desc, sub_provider_desc, i)
        post_api_caller(df.loc[i].to_json())


if __name__ == '__main__':
    sys.exit(main())
