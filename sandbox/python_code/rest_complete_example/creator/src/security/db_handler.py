#!/usr/bin/env python

import psycopg2


class SecurityDBHandler:

    def connect(self):
        self.conn = psycopg2.connect(
            host="openbsd.64",
            database="pgdb1",
            user="kkv1",
            password="point007")

        print('connected to db: ' + str(self.conn))

    def next_sequence_value(self):
        cur = self.conn.cursor()
        cur.execute("select nextval('securitydbo.master_id_seq')")
        self.master_id = cur.fetchone()[0]
        cur.close()
        return self.master_id

    def check_security(self, master_id):
        cur = self.conn.cursor()
        cur.execute('''select count(*) from securitydbo.master where
                       master_id = %s''', [master_id])
        cnt = cur.fetchone()[0]
        return cnt

    def db_insert(self, data):
        cur = self.conn.cursor()
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
        cur.close()

    def close(self):
        self.conn.close()

    def db_update(self, data):
        cur = self.conn.cursor()
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
        cur.close()

    def db_delete(self, data):
        cur = self.conn.cursor()
        cur.execute('''Delete From securitydbo.master
                        Where master_id = %s
                        ''',
                    data)
        self.conn.commit()
        cur.close()

    def db_query(self, data):
        cur = self.conn.cursor()

        cur.execute('''select
                        master_id, provider_desc, sub_provider_desc, security_name,
                        security_type, rating, isin, cusip, cins, live_cusip, sedol,
                        bbc_ticker, wkn, insert_ts, update_ts
                       from
                        securitydbo.master
                       where
                        master_id = %s
                    ''', data)
        (master_id, provider_desc, sub_provider_desc, security_name,
         security_type, rating, isin, cusip, cins, live_cusip, sedol,
         bbc_ticker, wkn, insert_ts, update_ts) = cur.fetchone()
        cur.close()

        return master_id, provider_desc, sub_provider_desc, security_name, \
        security_type, rating, isin, cusip, cins, live_cusip, sedol, \
        bbc_ticker, wkn, insert_ts, update_ts
