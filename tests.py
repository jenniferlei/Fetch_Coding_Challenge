"""Tests for fetch rewards app."""

from unittest import TestCase
import os
from flask import session
from server import app
from model import (connect_to_db, db, example_data)


class FlaskTestsBasic(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config["TESTING"] = True

    def test_index(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertIn(b"Earn points and rewards while you shop!", result.data)


class FlaskTestsDatabase(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "key"
        os.system("dropdb testdb --if-exists")
        os.system("createdb testdb")
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        example_data()
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess["username"] = "test"

    def tearDown(self):
        """Do at end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    def test_points_balance(self):
        """Test points balance page."""

        result = self.client.get("/point_balance.json")
        self.assertIn(b'{"DANNON":1100,"MILLER COORS":10000,"UNILEVER":200}', result.data)

    def test_spend_points(self):
        """Test spend points route."""

        result = self.client.post("/spend_points.json",
                                json={"points": 5000})
        self.assertIn(b'{"payer":"DANNON","points":-100}', result.data)
        self.assertIn(b'{"payer":"UNILEVER","points":-200}', result.data)
        self.assertIn(b'{"payer":"MILLER COORS","points":-4700}', result.data)

    def test_add_points(self):
        """Test add points route."""

        result = self.client.post("/add_points.json",
                                  json={"payer": "UNILEVER", "points": "300", "timestamp": "2021-10-31T10:00:00Z"})
        self.assertIn(b'{"payer":"UNILEVER","points":300,"timestamp":"2021-10-31T10:00:00"}', result.data)


class FlaskTestsLogInLogOut(TestCase):
    """Test log in and log out."""

    def setUp(self):
        """Before every test"""

        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "key"
        os.system("dropdb testdb --if-exists")
        os.system("createdb testdb")
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        example_data()
        self.client = app.test_client()

    def test_login(self):
        """Test login route."""
        with self.client as c:
            result = c.post("/login",
                            data={"username": "test"},
                            follow_redirects=True)
            self.assertIn(b"Welcome, test", result.data)

    def test_logout(self):
        """Test logout route."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess["username"] = "user"

            result = c.get("/logout",
                            follow_redirects=True,
                            headers={"Referer": "/"})

            self.assertNotIn(b"username", session)
            self.assertIn(b"Earn points and rewards while you shop!", result.data)


if __name__ == "__main__":
    import unittest

    unittest.main()
