"""Server for fetch rewards app."""

from flask import Flask, render_template, json, jsonify, request, flash, session, redirect
from flask_sqlalchemy import SQLAlchemy
from jinja2 import StrictUndefined
from datetime import datetime
import os

from model import Transaction, db, connect_to_db

from flask_marshmallow import Marshmallow
from marshmallow import fields

app = Flask(__name__)
ma = Marshmallow(app)

app.secret_key = "dev"
# app.secret_key = os.environ["APP_SECRET_KEY"]
app.jinja_env.undefined = StrictUndefined


class TransactionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Transaction
        load_instance = True


@app.route("/")
def homepage():
    """View homepage."""

    return render_template("index.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Process user login"""
    username = request.form.get("username")

    session["username"] = username
    flash(f"Welcome back, {username}!")

    return redirect(request.referrer)


@app.route("/logout")
def logout():
    """Logout and redirect homepage."""

    session.clear()

    return redirect("/")


@app.route("/point_balance.json")
def point_balance():
    """Return JSON response of available points per payer."""
    # A subsequent call to the points balance route, after the spend,
    # should returns the following results:
    # {
    # "DANNON": 1000,
    # "UNILEVER": 0,
    # "MILLER COORS": 5300
    # }

    username = session.get("username")
    transactions = Transaction.find_transactions_by_user(username)

    balances = {}

    for transaction in transactions:
        balances[transaction.payer] = balances.get(transaction.payer, 0) + transaction.balance

    return jsonify(balances)


@app.route("/add_points.json", methods=["POST"])
def add_points():
    """Add points"""
    # Suppose you call your add transaction route with the following sequence of calls:
    # ● { "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z" }
    # ● { "payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z" }
    # ● { "payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z" }
    # ● { "payer": "MILLER COORS", "points": 10000, "timestamp": "2020-11-01T14:00:00Z" }
    # ● { "payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z" }
    username = session.get("username")
    payer = request.get_json().get("payer")
    points = int(request.get_json().get("points"))
    timestamp = request.get_json().get("timestamp")

    new_transaction = Transaction.create_transaction(username, payer, points, timestamp, points)
    db.session.add(new_transaction)
    db.session.commit()

    # Define output format with marshmallow to match fields in example
    transaction_schema = TransactionSchema(exclude=["transaction_id", "username", "balance"])
    transaction_json = transaction_schema.dump(new_transaction)
    return jsonify(transaction_json)


@app.route("/spend_points.json", methods=["POST"])
def spend_points():
    """Create a reservation with the specified user and time."""
    # Then you call your spend points route with the following request:
    # { "points": 5000 }
    # The expected response from the spend call would be:
    # [
    # { "payer": "DANNON", "points": -100 },
    # { "payer": "UNILEVER", "points": -200 },
    # { "payer": "MILLER COORS", "points": -4,700 }
    # ]

    username = session.get("username", None)

    points = int(request.get_json().get("points"))
    timestamp = datetime.now()

    spend_calls = []

    # get transactions with balance greater than 0 and ordered by timestamp oldest to newest
    # Transaction(username=username, payer="DANNON", points=300, timestamp="2020-10-31T10:00:00Z", balance=100)
    # Transaction(username=username, payer="UNILEVER", points=200, timestamp="2020-10-31T11:00:00Z", balance=200)
    # Transaction(username=username, payer="MILLER COORS", points=10000, timestamp="2020-11-01T14:00:00Z", balance=10000)
    # Transaction(username=username, payer="DANNON", points=1000, timestamp="2020-11-02T14:00:00Z", balance=1000)
    transactions = Transaction.retrieve_transactions_with_balance(username)

    for transaction in transactions:
        if points > 0:
            # if the transaction balance is greater than spend points, spend down all points
            if transaction.balance > points:
                spend = points
            # if the spend points is greater than transaction balance, spend down transaction balance
            else:
                spend = transaction.balance
            # update balance on transaction
            transaction.balance -= spend
            # create new transaction for each spend
            spend_transaction = Transaction.create_transaction(username, transaction.payer, -spend, timestamp, 0)
            db.session.add(spend_transaction)
            db.session.commit()

            # Define output format to match fields in example
            spend_calls.append({"payer": transaction.payer, "points": -spend})

            # remove points that have been spent
            points -= spend

    return jsonify(spend_calls)


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

connect_to_db(app)