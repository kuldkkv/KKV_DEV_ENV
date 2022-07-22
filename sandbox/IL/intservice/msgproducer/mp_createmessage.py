import json
import hashlib

def create_message(row, batch_id, message_id, current_row, total_row, datetime):
    header = {
        'batch_id': batch_id,
        'message_id': message_id,
        'current_row': current_row,
        'total_row': total_row,
        'create_time': datetime
    }

    mesg = { 'header': header, 'data': row }

    json_mesg = json.dumps(mesg)
    checksum = hashlib.sha256(json_mesg.encode()).hexdigest()

    mesg = { 'checksum': checksum, 'header': header, 'data': row }
    json_mesg = json.dumps(mesg, indent = 4)

    return json_mesg

