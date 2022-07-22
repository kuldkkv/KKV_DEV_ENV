

def create_batch(conn, batch_name, eff_dt, status):
    cur = conn.cursor()

    seq_stmt = "select nextval('seq_batch_load')"
    cur.execute(seq_stmt)
    batch_id = cur.fetchone()[0]
    print('batch_id = ', batch_id)
    insert_stmt = "insert into batch_load (batch_load_id, batch_name, eff_dt, status, start_ts, end_ts, update_ts) values (%d, '%s', to_date('%s', 'YYYYMMDD'), '%s', current_timestamp, null, current_timestamp)" % (batch_id, batch_name, eff_dt, status)
                    
    cur.execute(insert_stmt)
    conn.commit()
    cur.close()
    return batch_id


def close_batch(conn, batch_id, status, mesg):
    cur = conn.cursor()

    mesg = mesg.replace("'", "''")
    upd_stmt = "update batch_load set status = '%s', mesg = '%s', update_ts = current_timestamp where batch_load_id = %d" % (status, mesg, batch_id)
    cur.execute(upd_stmt)