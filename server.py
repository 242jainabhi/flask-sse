from gevent import monkey;

monkey.patch_all()
from flask import Flask, Response, render_template, request
from gevent.pywsgi import WSGIServer
from flask_sqlalchemy import SQLAlchemy
import json
import time
from datetime import datetime
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Transaction(db.Model):
    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(100), nullable=False)
    merchant = db.Column(db.String(100), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(20), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


##############################

@app.route("/", methods=['GET', 'POST'])
def render():
    entries = {}
    if request.method == 'POST' and request.form['trans_id']:
        transaction_id = request.form['trans_id']
        entries = Transaction().query.filter_by(id=transaction_id).all()
    return render_template("index.html", entries=entries)


users = [f"User_{i}" for i in range(1, 11)]
merchants = [f"Merchant_{i}" for i in range(1, 11)]
currencies = ["INR", "USD", "EUR", "RUB", "MUR", "SGD"]


@app.route("/listen")
def listen():
    def respond_to_client():
        while True:
            global users, merchants, currencies
            random.shuffle(users)
            random.shuffle(merchants)
            random.shuffle(currencies)
            curr_time = datetime.utcnow()
            amount = random.randint(100, 1000)
            product_id = random.randint(100, 1000)
            quantity = random.randint(100, 1000)

            trans_obj = Transaction(user=users[0], merchant=merchants[0], time=curr_time, amount=amount,
                                    currency=currencies[0], product_id=product_id, quantity=quantity)
            db.session.add(trans_obj)
            db.session.commit()

            _data = json.dumps({"id": trans_obj.id, "user": users[0], "merchant": merchants[0], "time": str(curr_time),
                                "amount": amount, "currency": currencies[0], "product_id": product_id, "quantity": quantity})

            yield f"id: 1\ndata: {_data}\nevent: online\n\n"
            time.sleep(0.06)

    return Response(respond_to_client(), mimetype='text/event-stream')


if __name__ == "__main__":
    http_server = WSGIServer(("localhost", 5000), app)
    try:
        print('starting server')
        http_server.serve_forever()
        print('done with server')
    except (KeyboardInterrupt, SystemExit):
        print('Shutting down on interrupt...')

        if http_server.started:
            http_server.stop()
    finally:
        print('Shutting down.')
