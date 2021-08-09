# Realtime Transaction Generator

- Server Sent Events: As there is only one way communication
- Server: Python Flask
- Client: Javascript
- Database: SQLite (with SQLAlchemy ORM)

Reason to use SSE:
Since application sends data in one direction (server to client), SSE is a good option.


Steps to execute:
1) clone this repo
2) install `Python 3.x`
3) [can use virtual environment]
4) pip install -r requirements.txt
5) To create the initial database and tables, from an interactive Python shell,
   run `from server import db` and `db.create_all()`.
6) `python server.py`
7) go to browser and hit `http://localhost:5000`

Areas of improvements:
1) The server stops generating the transactions as soon as the client disconnects.
   This should be improved as the transaction generation should be independent of client connection.
2) When we refresh the client or search a transaction, the transaction table refreshes.
