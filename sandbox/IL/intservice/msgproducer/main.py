#!/usr/bin/env python

from datetime import datetime
import sys

import mp_readmetadata
import mp_connection
import mp_srcdatareader
import mp_createmessage
import batch
import control_master


def main():
    try:
        datetime_format = "%Y%m%d_%H%M%S.%f"
        batch_id = None

        conn = mp_connection.get_connection()
        batch_id = batch.create_batch(conn, 'TEST1', '20220722', 'RUNNING')
        print('batch_id is : ', batch_id)
        metadata_dict = mp_readmetadata.read_metadata(conn, 1)
        print(metadata_dict)
        current_row = 1 
        total_row = -1

        cur = conn.cursor()

        for row in mp_srcdatareader.data_reader(conn, metadata_dict):
            message_id = str(batch_id) + '_' + str(current_row)
            json_mesg = mp_createmessage.create_message(row, batch_id, message_id, current_row, total_row, 
                            datetime.now().strftime(datetime_format))
            control_master.insert(cur, batch_id, message_id, current_row, json_mesg, False)
            current_row += 1
        batch.close_batch(conn, batch_id, 'SUCCESS', "")
    except Exception as e:
        if batch_id:
            conn.commit()
            batch.close_batch(conn, batch_id, 'FAILED', str(e))
        raise
    finally:
        if batch_id:
            cur.close()
            conn.commit()
            conn.close()




if __name__ == '__main__':
    main()

