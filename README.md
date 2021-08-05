# Realtime Transaction Generator

- Server Sent Events: As there is only one way communication
- Server: Python Flask
- Client: Javascript
- Database: SQLite (with SQLAlchemy ORM)

Steps to execute:
1) clone this repo
2) install `Python 3.x`
3) [can use virtual environment]
4) pip install -r requirements.txt
5) To create the initial database and tables, from an interactive Python shell,
   run `from server import db` and `db.create_all()`.
6) `python server.py`
7) go to browser and hit `http://localhost:5000`
