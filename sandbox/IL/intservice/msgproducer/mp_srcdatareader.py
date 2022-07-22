import mp_todict

def data_reader(conn, metadata_dict):
    sql_text = metadata_dict['sql_text']
    cur = conn.cursor()
    print(cur, conn)
    
    cur = conn.cursor(name = 'server_side_fetch')
    cur.execute(sql_text)

    while True:
        rows = cur.fetchmany(size = 500)
        col_names = [ desc[0] for desc in cur.description ]

        if not rows:
            break

        for row in rows:
            dict = mp_todict.to_dict(col_names, row)
            yield(dict)

    cur.close()
