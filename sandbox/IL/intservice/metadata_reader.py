#!/usr/bin/env python


import psycopg2


def read_metadata(metadata_id):
    conn = psycopg2.connect(
            database='intg_layer', user = 'stage', password = 'point007', host = 'rocky')

    print('connected to database')
    cur = conn.cursor()

    sql = '''
        Select src_platform, sql_text, insert_ts from il_metadata
    '''
    cur.execute(sql)

    data = cur.fetchone()
    print(data);
    src_sql = data[1];
    cur.execute(src_sql);
    col_names = [desc[0] for desc in cur.description]
    print(col_names)
    print('source sql resultset')

    i = 1
    itr = 1
    while (data):
        data = cur.fetchmany(20)
        col_names = [desc[0] for desc in cur.description]
        for r in data:
            print('Itr', itr, 'No ', i, '--> ', r)
            i = i+1
        itr = itr + 1
    
    print(col_names)
    conn.close()


