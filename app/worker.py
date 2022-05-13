import logging
import redis

from flask import Flask

from rq import Worker, Queue, Connection

from databases import db_session
from models import Message


def store_message(text, time):
    try:
        queued_message = Message(text, time)
        db_session.add(queued_message)
        db_session.commit()
    except Exception:
        logging.error("Could not store message '%s', \
                      check your database settings." % text)
        raise


app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Remove sessions at end of request
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


listen = ['default']

try:
    conn = redis.from_url(app.config["REDIS_URL"])
except Exception:
    logging.error("Your REDIS_URL setting is invalid")

if __name__ == '__main__':
    try:
        with Connection(conn):
            worker = Worker(list(map(Queue, listen)))
            worker.work()
    except Exception:
        logging.error("Your Redis database is unreachable. Process ending...")
