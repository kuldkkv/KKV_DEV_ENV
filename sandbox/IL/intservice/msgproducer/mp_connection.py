import psycopg2

def get_connection():
    conn = psycopg2.connect(
        database='intg_layer', user = 'stage', password = 'point007', host = 'rocky'
    )
    return conn
