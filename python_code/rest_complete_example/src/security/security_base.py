#!/usr/bin/env python

import datetime
from flask import jsonify
from db_handler import SecurityDBHandler


class SecurityBase:
    def __init__(self, provider_desc, sub_provider_desc, security_name,
                 security_type, rating, isin, cusip, cins, live_cusip, sedol,
                 bbc_ticker, wkn, master_id):
        self.provider_desc = provider_desc
        self.sub_provider_desc = sub_provider_desc
        self.security_name = security_name
        self.security_type = security_type
        self.rating = rating
        self.isin = isin
        self.cusip = cusip
        self.cins = cins
        self.live_cusip = live_cusip
        self.sedol = sedol
        self.bbc_ticker = bbc_ticker
        self.wkn = wkn
        self.master_id = master_id
        self.status = None
        self.errm = ''
        self.return_message = ''
        self.message_detail = ''
        self.security_ref_json = None
        self.sec_db_handler = SecurityDBHandler()

        print('init done')

    def __create_db_connection(self):
        self.sec_db_handler.connect()


    def __valid_security_request(self):
        self.status = True
        if not self.provider_desc or not self.sub_provider_desc or not self.security_name or not self.security_type:
            self.status = False
            self.errm = "ERROR_MANDATORY_FIELDS"
        if not (
                self.isin or self.cusip or self.cins or self.live_cusip or self.sedol or self.bbc_ticker or self.wkn):
            self.status = False
            self.errm = "ERROR_NO_XREF"

        print('in validation, security status is ' + str(self.status))
        return self.status

    def __create_new_master_id(self):
        self.master_id = self.sec_db_handler.next_sequence_value()
        return self.master_id

    def __insert_new_security_in_db(self):
        self.current_tm = datetime.datetime.now()
        data = [self.master_id, self.provider_desc, self.sub_provider_desc, self.security_name,
                self.security_type, self.rating, self.isin, self.cusip, self.cins, self.live_cusip, self.sedol, self.bbc_ticker, self.wkn, self.current_tm, self.current_tm]

        self.sec_db_handler.db_insert(data)

        print('new security inserted')

    def __close_db_connection(self):
        self.sec_db_handler.close()


    def __update_security_in_db(self):
        self.current_tm = datetime.datetime.now()
        data = [self.provider_desc, self.sub_provider_desc, self.security_name,
                self.security_type, self.rating, self.isin, self.cusip, self.cins, self.live_cusip, self.sedol, self.bbc_ticker, self.wkn, self.current_tm, self.master_id]
        self.sec_db_handler.db_update(data)
        print('security updated')

    def __is_existing_security(self):
        if self.master_id == '':
            return 0
        cnt = self.sec_db_handler.check_security(self.master_id)
        print('security existance count is:', cnt)
        return cnt


    def __delete_security_in_db(self):
        data = [self.master_id]
        self.sec_db_handler.db_delete(data)
        print('security deleted')


    def __get_security_from_db(self):
        data = [self.master_id]
        (self.master_id, self.provider_desc, self.sub_provider_desc, self.security_name,
         self.security_type, self.rating, self.isin, self.cusip, self.cins, self.live_cusip, self.sedol,
         self.bbc_ticker, self.wkn, self.insert_ts, self.update_ts) = self.sec_db_handler.db_query(data)
