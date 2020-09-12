#!/usr/bin/env python

import psycopg2
import datetime
from flask import jsonify
from security_base import SecurityBase


class Security(SecurityBase):
    def __init__(self, provider_desc, sub_provider_desc, security_name,
                 security_type, rating, isin, cusip, cins, live_cusip, sedol,
                 bbc_ticker, wkn, master_id):

        super().__init__(provider_desc, sub_provider_desc, security_name,
                 security_type, rating, isin, cusip, cins, live_cusip, sedol,
                 bbc_ticker, wkn, master_id)
        print('init done')


    def create_security(self):
        if not super()._SecurityBase__valid_security_request():
            print('validation failed returning : ' + str(self.status))
            self.return_message = 'Security creation failed'
            self.message_detail = 'New security creation failed at attribute validation step'
            return self.status

        super()._SecurityBase__create_db_connection()
        super()._SecurityBase__create_new_master_id()
        super()._SecurityBase__insert_new_security_in_db()
        super()._SecurityBase__close_db_connection()
        self.status = True
        self.errm = 'OK'
        self.return_message = 'New secuity sucessfully created'
        self.message_detail = 'New secuity sucessfully created'

        return self.status


    def update_security(self):
        print('in update function')
        if not super()._SecurityBase__valid_security_request():
            print('validation failed returning : ' + str(self.status))
            self.return_message = 'Security updation failed'
            self.message_detail = 'Security updation failed at attribute validation step'
            return self.status

        super()._SecurityBase__create_db_connection()
        if super()._SecurityBase__is_existing_security() == 0:
            print('security does not exists')
            self.return_message = 'Security updation failed'
            self.message_detail = 'Security does not exists'
            return self.status

        super()._SecurityBase__update_security_in_db()
        super()._SecurityBase__close_db_connection()
        self.status = True
        self.errm = 'OK'
        self.return_message = 'Secuity updated sucessfully created'

        return self.status


    def delete_security(self):
        print('in delete function')
        super()._SecurityBase__create_db_connection()
        if super()._SecurityBase__is_existing_security() == 0:
            print('security does not exists')
            self.return_message = 'Security deletion failed'
            self.message_detail = 'Security does not exists'
            return self.status

        super()._SecurityBase__delete_security_in_db()
        super()._SecurityBase__close_db_connection()
        self.status = True
        self.errm = 'OK'
        self.return_message = 'Secuity deleted sucessfully created'

        return self.status


    def get_security(self):
        print('in get function')
        super()._SecurityBase__create_db_connection()
        if super()._SecurityBase__is_existing_security() == 0:
            print('security does not exists')
            self.return_message = 'Security get failed'
            self.message_detail = 'Security does not exists'
            return self.status
        super()._SecurityBase__get_security_from_db()
        super()._SecurityBase__close_db_connection()
        self.status = True
        self.errm = 'OK'
        self.return_message = 'Secuity fetched sucessfully'

        self.security_ref_json = {
            'master_id' : self.master_id,
            'provider_desc' : self.provider_desc,
            'sub_provider_desc' : self.sub_provider_desc,
            'security_name' : self.security_name,
            'security_type' : self.security_type,
            'rating' : self.rating,
            'isin' : self.isin,
            'cusip' : self.cusip,
            'cins' : self.cins,
            'live_cusip' : self.live_cusip,
            'sedol' : self.sedol,
            'bbc_ticker' : self.bbc_ticker,
            'wkn' : self.wkn,
            'insert_ts' : self.insert_ts,
            'update_ts' : self.update_ts
        }

        return self.status
