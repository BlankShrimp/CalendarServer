from flask import Flask, request, Response
import dao
import json


app = Flask(__name__)

@app.route('/begin', methods=['GET'])
def begin():
    return Response(status=200)


@app.route('/events', methods=['GET'])
def get_events():
    args = request.args
    if 'timestamp' in args:
        latest, data = dao.sync_new_entries(args['timestamp'])
        return Response(str(latest)+json.dumps(data), status=200)
    else:
        latest, data = dao.fetch_all_valid_entries()
        return Response(str(latest)+json.dumps(data), status=200)


if __name__ == "__main__": 
    dao.init_db_if_not_exists()
    app.run(debug = True, port = 80, host = '0.0.0.0')