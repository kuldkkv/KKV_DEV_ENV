#!/usr/bin/env python


import mp_todict


def read_metadata(conn, metadata_id):
    cur = conn.cursor()

    sql = '''
        Select src_platform, sql_text, insert_ts from il_metadata
    '''
    cur.execute(sql)

    col_names = [desc[0] for desc in cur.description]
    data = cur.fetchone()
    dict = mp_todict.to_dict(col_names, data)
    
    print(dict);

    cur.close()
    return dict

