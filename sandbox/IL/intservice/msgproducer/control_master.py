
def insert(cur, batch_load_id, message_id, current_row, json_mesg, sent_to_queue):

    json_mesg = json_mesg.replace("'", "''")
    insert_stmt = "insert into control_master (control_master_id, batch_load_id, message_id, current_row, message, sent_to_queue, sent_to_queue_ts, update_ts) values (nextval('seq_control_master'), %d, '%s', %d, '%s', %s, current_timestamp, current_timestamp)" % (batch_load_id, message_id, current_row, json_mesg, sent_to_queue)
                    
    cur.execute(insert_stmt)
