#!/usr/bin/env python

import psycopg2
import datetime


class Security:
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
        self.conn = None
        self.master_id = master_id
        self.status = None
        self.errm = ''
        self.return_message = ''
        self.message_detail = ''

        print('init done')

    def create_db_connection(self):
        self.conn = psycopg2.connect(
            host="openbsd.64",
            database="pgdb1",
            user="kkv1",
            password="point007")

        print('connected to db: ' + str(self.conn))

    def valid_security_request(self):
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

    def create_new_master_id(self):
        cur = self.conn.cursor()
        cur.execute("select nextval('securitydbo.master_id_seq')")
        self.master_id = cur.fetchone()[0]
        cur.close()
        return self.master_id

    def insert_new_security_in_db(self):
        cur = self.conn.cursor()
        self.current_tm = datetime.datetime.now()
        data = [self.master_id, self.provider_desc, self.sub_provider_desc, self.security_name,
                self.security_type, self.rating, self.isin, self.cusip, self.cins, self.live_cusip, self.sedol, self.bbc_ticker, self.wkn, self.current_tm, self.current_tm]
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
        self.conn.commit()
        print('new security inserted')
        cur.close()

    def close_db_connection(self):
        self.conn.close()

    def create_security(self):
        if not self.valid_security_request():
            print ('validation failed returning : ' + str(self.status))
            self.return_message = 'Security creation failed'
            self.message_detail = 'New security creation failed at attribute validation step'
            return self.status

        self.create_db_connection()
        self.create_new_master_id()
        self.insert_new_security_in_db()
        self.close_db_connection()
        self.status = True
        self.errm = 'OK'
        self.return_message = 'New secuity sucessfully created'
        self.message_detail = 'New secuity sucessfully created'

        return self.status



    def update_security_in_db(self):
        cur = self.conn.cursor()
        self.current_tm = datetime.datetime.now()
        data = [self.provider_desc, self.sub_provider_desc, self.security_name,
                self.security_type, self.rating, self.isin, self.cusip, self.cins, self.live_cusip, self.sedol, self.bbc_ticker, self.wkn, self.current_tm, self.master_id]
        cur.execute('''Update securitydbo.master set
                        provider_desc = %s,
                        sub_provider_desc = %s,
                        security_name = %s,
                        security_type = %s,
                        rating = %s,
                        isin = %s,
                        cusip = %s,
                        cins = %s,
                        live_cusip = %s,
                        sedol = %s,
                        bbc_ticker = %s,
                        wkn = %s,
                        update_ts = %s
                        Where master_id = %s
                        ''',
                    data)
        self.conn.commit()
        print('security updated')
        cur.close()

    def is_existing_security(self):
        cur = self.conn.cursor()
        cur.execute('''select count(*) from securitydbo.master where
                       master_id = %s''', [self.master_id])
        cnt = cur.fetchone()[0]
        print('security existance count is:', cnt)
        return cnt


    def update_security(self):
        print('in update function')
        if not self.valid_security_request():
            print ('validation failed returning : ' + str(self.status))
            self.return_message = 'Security updation failed'
            self.message_detail = 'Security updation failed at attribute validation step'
            return self.status

        self.create_db_connection()
        if self.is_existing_security() == 0:
            print('security does not exists')
            self.return_message = 'Security updation failed'
            self.message_detail = 'Security does not exists'
            return self.status

        self.update_security_in_db()
        self.close_db_connection()
        self.status = True
        self.errm = 'OK'
        self.return_message = 'Secuity updated sucessfully created'

        return self.status
