import sqlite3, time


def init_db_if_not_exists():
    conn = sqlite3.connect('calender.db')
    cursor = conn.cursor()
    cursor.execute('''create table if not exists 
        events(timestamp integer primary key, 
        start_time integer, 
        expire_time integer,
        content text, 
        hashvalue text)''')
    conn.commit()
    conn.close()


def insert_entry(timestamp, activision, expiry, content, hashvalue):
    conn = sqlite3.connect('calender.db')
    cursor = conn.cursor()
    params = (timestamp, activision, expiry, content, hashvalue)
    cursor.execute("insert into events (timestamp, start_time, expire_time, content, hashvalue) values (?, ?, ?, ?, ?)", params)
    conn.commit()
    conn.close()
    return


def fetch_all_valid_entries():
    conn = sqlite3.connect('calender.db')
    cursor = conn.cursor()
    cursor.execute("select * from events where expire_time > %s order by start_time"%(int(time.time())))
    data = []
    latest = 0
    for row in cursor:
        latest =  row[0] if row[0] > latest else latest
        data.append({'start_time': row[1], 'expire_time': row[2], 'content': row[3], 'hashvalue': row[4]})
    conn.close()
    return latest, data


def sync_new_entries(timestamp):
    conn = sqlite3.connect('calender.db')
    cursor = conn.cursor()
    cursor.execute("select * from events where timestamp > %s and expire_time > %s order by start_time"%(timestamp, int(time.time())))
    data = []
    latest = 0
    for row in cursor:
        latest =  row[0] if row[0] > latest else latest
        data.append({'start_time': row[1], 'expire_time': row[2], 'content': row[3], 'hashvalue': row[4]})
    conn.close()
    return latest, data


def fetch_all_valid_hashvalues():
    conn = sqlite3.connect('calender.db')
    cursor = conn.cursor()
    cursor.execute("select hashvalue from events where expire_time > %s order by start_time"%(int(time.time())))
    data = []
    for row in cursor:
        data.append(row[0])
    conn.close()
    return data


def eliminate_by_hashvalue(hashvalue): 
    conn = sqlite3.connect('calender.db')
    cursor = conn.cursor()
    cursor.execute("update events set expire_time = %s where hashvalue = '%s'"%(int(time.time()), hashvalue))
    conn.commit()
    result = True if conn.total_changes != 0 else False
    return result