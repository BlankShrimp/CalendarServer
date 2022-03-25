from flask import Flask, request, Response
from hashlib import sha256
import dao
import json, time


app = Flask(__name__)
dao.init_db_if_not_exists()

@app.route('/begin', methods=['GET'])
def begin():
    return Response(status=200)


@app.route('/events', methods=['GET'])
def get_events(): # timestamp(optional)
    args = request.args
    if 'timestamp' in args:
        latest, data = dao.sync_new_entries(args['timestamp'])
        return Response(str(latest)+json.dumps(data), status=200)
    else:
        latest, data = dao.fetch_all_valid_entries()
        return Response(str(latest)+json.dumps(data), status=200)


@app.route('/add', methods=['POST'])
def post_event(): # start_time, expiry, content
    args = request.args
    if 'start_time' not in args or 'expiry' not in args or 'content' not in args:
        return Response(status=400)
    else:
        hashvalue = sha256((args['start_time'] + args['expiry'] + args['content']).encode('utf-8')).hexdigest()
        dao.insert_entry(int(time.time()), args['start_time'], args['expiry'], args['content'], hashvalue)
        return Response(status=201)


@app.route('/eliminate', methods=['POST'])
def eliminate_by_hashvalue(): #hashvalue
    args = request.args
    if 'hashvalue' not in args:
        return Response(status=400)
    else:
        target_hash = args['hashvalue']
        list_of_hashvalues = dao.fetch_all_valid_hashvalues()
        for candidate in list_of_hashvalues:
            if target_hash == candidate[:len(target_hash)]: 
                dao.eliminate_by_hashvalue(candidate)
                return Response(status=200)
        return Response(status=404)



if __name__ == "__main__": 
    app.run(debug = True, port = 80, host = '0.0.0.0')
