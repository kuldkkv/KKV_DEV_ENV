#!/usr/bin/env python

import psycopg2
import datetime


class Security:
    def __init__(self, provider_desc, sub_provider_desc, security_name,
                 security_type, rating, isin, cusip, cins, live_cusip, sedol,
                 bbc_ticker, wkn):
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
        self.master_id = None
        self.status = None
        self.errm = None
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
            return self.status

        self.create_db_connection()
        self.create_new_master_id()
        self.insert_new_security_in_db()
        self.close_db_connection()
        self.status = True
        self.errm = None

        return self.status
