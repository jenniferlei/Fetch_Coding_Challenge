"""Script to seed database."""

import os
import model
import server

# Run dropdb and createdb to re-create database
os.system("dropdb points --if-exists")
os.system("createdb points")

# Connect to the database and call db.create_all
model.connect_to_db(server.app)
model.db.create_all()

test_transactions = [
    model.Transaction(username="test",
                    payer="DANNON",
                    points=1000,
                    timestamp="2020-11-02T14:00:00Z",
                    balance=1000),
    model.Transaction(username="test",
                    payer="UNILEVER",
                    points=200,
                    timestamp="2020-10-31T11:00:00Z",
                    balance=200),
    model.Transaction(username="test,
                    payer="DANNON",
                    points=-200,
                    timestamp="2020-10-31T11:00:00Z",
                    balance=0),
    model.Transaction(username="test,
                    payer="MILLER COORS",
                    points=10000,
                    timestamp="2020-11-01T14:00:00Z",
                    balance=10000),
    model.Transaction(username="test,
                    payer="DANNON",
                    points=300,
                    timestamp="2020-10-31T10:00:00Z",
                    balance=100)
    ]
    
model.db.session.add_all(test_transactions)
model.db.session.commit()
