from unittest import TestCase
from flask import session
from server import app
from model import (connect_to_db, db, example_data)
import os

# Only need to do this once to test database:
os.system("dropdb testdb --if-exists")
os.system("createdb testdb")
# Connect to test database
connect_to_db(app, "postgresql:///testdb")
# Create tables and add sample data
db.create_all()
example_data()


class FlaskTestsBasic(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertIn(b"Welcome!", result.data)


class FlaskTestsDatabase(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Need a key when testing with sessions
        app.config['SECRET_KEY'] = 'key' 

        # # Only need to do this once to test database:
        # os.system("dropdb testdb --if-exists")
        # os.system("createdb testdb")

        # # Connect to test database
        # connect_to_db(app, "postgresql:///testdb")
        
        # # Create tables and add sample data
        # db.create_all()
        # example_data()

        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess["username"] = "test"

    def tearDown(self):
        """Do at end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    def test_login(self):
        """Test login page."""
        result = self.client.post("/login",
                                  data={"username": "test"},
                                  follow_redirects=True, headers={"Referer": "/"})
        self.assertIn(b"Log Out", result.data)

    def test_points_balance(self):
        """Test points balance page."""

        result = self.client.get("/point_balance.json")
        self.assertIn(b"\"DANNON\": 1100,", result.data)
        self.assertIn(b"\"MILLER COORS\": 10000,", result.data)
        self.assertIn(b"\"UNILEVER\": 200,", result.data)

    def test_add_points(self):
        """Test add points route."""

        result = self.client.post("/add_points.json",
                                  data={"username": "test"},
                                  follow_redirects=True, headers={"Referer": "/"})
        self.assertIn(b"Log Out", result.data)
        self.assertIn(b"Phone: 555-1000", result.data)

    def test_spend_points(self):
        """Test spend points route."""

        result = self.client.post("/spend_points.json",
                                  data={"points": 5000})
        self.assertIn(b"{ \"payer\": \"DANNON\", \"points\": -100 }", result.data)
        self.assertIn(b"{ \"payer\": \"UNILEVER\", \"points\": -200 }", result.data)
        self.assertIn(b"{ \"payer\": \"MILLER COORS\", \"points\": -4700 }", result.data)


class FlaskTestsLoggedIn(TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True

        # Need a key when testing with sessions
        app.config['SECRET_KEY'] = 'key'

        # # Only need to do this once to test database:
        # os.system("dropdb testdb --if-exists")
        # os.system("createdb testdb")

        # # Connect to test database
        # connect_to_db(app, "postgresql:///testdb")

        # # Create tables and add sample data
        # db.create_all()
        # example_data()

        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['username'] = "test"

    def test_logged_in(self):
        """Test dashboard page."""

        result = self.client.get("/")
        self.assertIn(b"Welcome, test", result.data)


class FlaskTestsLoggedOut(TestCase):
    """Flask tests with user logged out of session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        # # Only need to do this once to test database:
        # os.system("dropdb testdb --if-exists")
        # os.system("createdb testdb")

        # # Connect to test database
        # connect_to_db(app, "postgresql:///testdb")

        # # Create tables and add sample data
        # db.create_all()
        # example_data()

    def test_logged_out(self):
        """Test that user can't see dashboard page when logged out."""

        result = self.client.get("/", follow_redirects=True)
        self.assertIn(b"Log in to start making your melon tasting reservation today", result.data)


class FlaskTestsLogInLogOut(TestCase):
    """Test log in and log out."""

    def setUp(self):
        """Before every test"""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'

        # # Only need to do this once to test database:
        # os.system("dropdb testdb --if-exists")
        # os.system("createdb testdb")

        # # Connect to test database
        # connect_to_db(app, "postgresql:///testdb")

        # # Create tables and add sample data
        # db.create_all()
        # example_data()

        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['username'] = "testuser0"
                sess['login'] = True

    def test_login(self):
        """Test log in form.

        Unlike login test above, 'with' is necessary here in order to refer to session.
        """

        with self.client as c:
            
            result = c.post('/login',
                            data={"username": "testuser0"},
                            follow_redirects=True,
                            headers={"Referer": "/"}
                            )
            self.assertEqual(session['username'], 'testuser0')
            self.assertEqual(session['login'], True)
            self.assertIn(b"Welcome back", result.data)

    def test_logout(self):
        """Test logout route."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['username'] = 'testuser0'

            result = c.get("/logout",
                            follow_redirects=True,
                            headers={"Referer": "/"})

            self.assertNotIn(b'username', session)
            self.assertNotIn(b'login', session)
            # print("LINE 207", result.data)
            self.assertIn(b'Successfully logged out!', result.data)


if __name__ == "__main__":
    import unittest

    unittest.main()
