import sqlite3, time, json


def init_db_if_not_exists():
    conn = sqlite3.connect('calender.db')
    cursor = conn.cursor()
    cursor.execute('''create table if not exists 
        events(timestamp integer primary key, 
        activite_time integer, 
        expire_time integer,
        content text)''')
    cursor.execute('''create table if not exists 
        credentials(uuid text primary key, 
        pubkey text)''')
    conn.commit()
    conn.close()


def insert_entry(timestamp, activision, expiry, content):
    conn = sqlite3.connect('calender.db')
    cursor = conn.cursor()
    params = (timestamp, activision, expiry, content)
    cursor.execute("insert into events (timestamp, activite_time, expire_time, content) values (?, ?, ?, ?)", params)
    conn.commit()
    conn.close()
    return


def fetch_all_valid_entries():
    conn = sqlite3.connect('calender.db')
    cursor = conn.cursor()
    cursor.execute("select * from events where expire_time > %s order by activite_time"%(int(time.time())))
    data = []
    latest = 0
    for row in cursor:
        latest =  row[0] if row[0] > latest else latest
        data.append({'activite_time': row[1], 'expire_time': row[2], 'content': row[3]})
    conn.close()
    return latest, data


def sync_new_entries(timestamp):
    conn = sqlite3.connect('calender.db')
    cursor = conn.cursor()
    cursor.execute("select * from events where timestamp > %s and expire_time > %s order by activite_time"%(timestamp, int(time.time())))
    data = []
    latest = 0
    for row in cursor:
        latest =  row[0] if row[0] > latest else latest
        data.append({'activite_time': row[1], 'expire_time': row[2], 'content': row[3]})
    conn.close()
    return latest, data