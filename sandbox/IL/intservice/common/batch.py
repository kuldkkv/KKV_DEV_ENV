

def create_batch(conn, batch_name, eff_dt, status):
    cur = conn.cursor()

    insert_stmt = '''insert into batch_load 
                        (batch_load_id, batch_name, eff_dt, status, start_ts, end_ts, update_ts) 
                     values
                        (nextval('seq_batch_load'), %%s, to_date('%%s', 'YYYYMMDD'), %%s, current_timestamp, null, current_timestamp)
                    '''
    print(insert_stmt)
    cur.execute(insert_stmt, (batch_name, eff_dt, status))
    conn.commit()
    cur.close()
    return 1010