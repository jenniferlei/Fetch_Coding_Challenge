"""Model for fetch rewards app."""

import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# For Heroku Deployment
# uri = os.getenv("DATABASE_URL")
# if uri.startswith("postgres://"):
#     uri = uri.replace("postgres://", "postgresql://", 1)

other_uri = "postgresql:///points"

class Transaction(db.Model):
    """A transaction."""

    __tablename__ = "transactions"

    transaction_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, nullable=False)
    payer = db.Column(db.String, nullable=False)
    points = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    balance = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Transaction payer={self.payer} points={self.points} timestamp={self.timestamp} balance={self.balance}>"

    @classmethod
    def create_transaction(cls, username, payer, points, timestamp, balance):
        """Create a transaction."""

        transaction = Transaction(username=username, payer=payer, points=points, timestamp=timestamp, balance=balance)
        
        db.session.add(transaction)
        db.session.commit()

        return transaction

    @classmethod
    def find_transactions_by_user(cls, username):
        """Find all transactions by user."""

        transactions = Transaction.query\
            .filter(Transaction.username==username)\
            .all()

        return transactions

    @classmethod
    def retrieve_transactions_with_balance(cls, username):
        """Retrieve all transactions with balance greater than 0 for a user."""

        transactions = Transaction.query\
            .filter(Transaction.username==username)\
            .filter(Transaction.balance>0)\
            .order_by(Transaction.timestamp)\
            .all()

        return transactions


def connect_to_db(flask_app, db_uri=other_uri, echo=True):
    """Connect to database."""

    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


def example_data():
    """Create example data for the test database."""
    
    username = "test"

    test_transactions = [
        Transaction(username=username, payer="DANNON", points=1000, timestamp="2020-11-02T14:00:00Z", balance=1000),
        Transaction(username=username, payer="UNILEVER", points=200, timestamp="2020-10-31T11:00:00Z", balance=200),
        Transaction(username=username, payer="DANNON", points=-200, timestamp="2020-10-31T11:00:00Z", balance=0),
        Transaction(username=username, payer="MILLER COORS", points=10000, timestamp="2020-11-01T14:00:00Z", balance=10000),
        Transaction(username=username, payer="DANNON", points=300, timestamp="2020-10-31T10:00:00Z", balance=100)
        ]
        
    db.session.add_all(test_transactions)
    db.session.commit()


if __name__ == "__main__":

    from server import app

    connect_to_db(app)
    