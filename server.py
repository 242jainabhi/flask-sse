from gevent import monkey; monkey.patch_all()
from flask import Flask, Response, render_template, request
from gevent.pywsgi import WSGIServer
import json
import time
from datetime import datetime
import random

app = Flask(__name__)


@app.route("/")
def render():
    return render_template("index.html")


trans_id = 0
users = ["U1", "U2", "U3", "U4", "U5"]
merchants = ["M1", "M2", "M3", "M4", "M5"]
currencies = ["INR", "USD", "EUR"]


@app.route("/listen")
def listen():

    def respond_to_client():
        while True:
            global trans_id, users, merchants, currencies
            trans_id += 1
            random.shuffle(users)
            random.shuffle(merchants)
            random.shuffle(currencies)
            curr_time = datetime.utcnow()
            amount = random.randint(100, 500)

            _data = json.dumps({"id": trans_id, "user": users[0], "merchant": merchants[0], "time": str(curr_time),
                                "amount": amount, "currency": currencies[0]})
            
            yield f"id: 1\ndata: {_data}\nevent: online\n\n"
            time.sleep(0.06)
    return Response(respond_to_client(), mimetype='text/event-stream')


if __name__ == "__main__":
    http_server = WSGIServer(("localhost", 80), app)
    http_server.serve_forever()
