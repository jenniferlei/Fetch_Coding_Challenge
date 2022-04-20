# Fetch Rewards Coding Challenge

This project allows a user to add and spent points.

Fetch Rewards Coding Challenge is deployed on Heroku: <a href="https://fetch-coding-challenge.herokuapp.com/" target="_blank">https://fetch-coding-challenge.herokuapp.com/</a>

**CONTENTS**

- [Tech Stack](#tech-stack)
- [Justification](#justification)
- [Reflection](#reflection)
- [Installation](#installation)
- [About the Developer](#about-the-developer)

## Tech Stack

**Backend:** Python3, Flask, SQLAlchemy, Marshmallow, Jinja\
**Frontend:** JavaScript (React), HTML5, CSS3, Bootstrap\
**Database:** PostgreSQL

## Justification

I chose to use Flask, a lightweight web framework that is flexible and simple to implement. Although a durable data store was not required, I used postgreSQL because it is a commonly used relational database and allows for scalability, such as adding payer/partner information, user information, reward information, etc. SQLAlchemy allowed me to incorporate Flask and postrgresQL with Python. I used Marshmallow for serialization to create API endpoints. I used Jinja to generate my base HTML depending on session information and React to handle making calls to the points balance, adding points, and spending points so that the page does not need to reload after the user submits their query.

## Reflection

Currently, a user can log in without a password. Log in was outside the scope of the challenge, however, given more time, I would incorporate a User table that would have a relationship with the Transaction table. With a User table, I could have a password field which would allow me to enable authentication.

I added unit tests that test that each API endpoints return the correct results, as well as test the homepage, login and logout pages.

I added error handling on both frontend and backend for if a user leaves a form field blank or inputs an invalid number of points for either adding or spending (add/spend <= 0 or spend > points balance).
The user should not be able to access the forms if not logged in, but it may be possible if they have the app open on multiple tabs and logout from one tab. I added error handling on the backend for when the user submits a form when username is not in session.

## Installation

### Requirements:

- PostgreSQL
- Python 3.7.3

To run Fetch Rewards Coding Challenge on your local machine, follow the instructions below:

Clone repository:

```
$ git clone https://github.com/jenniferlei/Fetch_Coding_Challenge.git
```

Create and activate a virtual environment inside your project directory:

```
$ pip3 install virtualenv
$ virtualenv env (Mac OS)
$ virtualenv env --always-copy (Windows OS)
$ source env/bin/activate
```

Install the dependencies:

```
(env) pip3 install -r requirements.txt
```

(Optionally) Seed the database:

```
(env) python3 seed.py
```

Note: if you do not run `seed.py`, make sure you create a database named
points:
`createdb points`.

Create a secrets.sh file to assign a value to APP_SECRET_KEY and run it:

```
(env) source secrets.sh
```

Run the app:

```
(env) python3 server.py
```

You can now navigate to `localhost:5000/` to start adding and spending points!

## About the Developer

Jennifer Lei is a software engineer in the Greater Los Angeles Area, and previously worked in multiple fields, such as B2B tech sales, finance and e-commerce. She decided to follow her dreams, pivoted to software engineering, and has enjoyed every minute of it since!

<p><a href="https://www.linkedin.com/in/jenniferlei/">
  <img
    alt="LinkedIn"
    src="https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white"
  />
</a>
<a href="https://twitter.com/JenniferLei_">
  <img
    alt="Twitter"
    src="https://img.shields.io/badge/twitter-%231DA1F2.svg?&style=for-the-badge&logo=twitter&logoColor=white"
  />
</a></p>
