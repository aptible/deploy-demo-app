import logging
import os
import signal

from datetime import datetime
from flask import Flask, redirect, request, render_template
from flask_wtf import FlaskForm
from functools import reduce
from psycopg2 import OperationalError
from redis.exceptions import ConnectionError, TimeoutError
from rq import Queue
from sqlalchemy.exc import InvalidRequestError
from wtforms import SubmitField, StringField

from databases import db_session
from models import Message
from models import Guidestep
from worker import conn
from worker import store_message

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'swiggityswooty'
queue = Queue(connection=conn)
logging.basicConfig(level=logging.DEBUG)


@app.teardown_appcontext
def shutdown_session(exception=None):
    """ Remove sessions at end of request """
    db_session.remove()


class InputForm(FlaskForm):
    """ This form is used to submit information from a webpage """
    message = StringField("Your message")
    submit = SubmitField("Send")


def read_messages(text, number):
    """ This will retrieve messages from the database
    if you specify a text, you will get the last number messages
    if you do not specify a text, you will get a single messge:
    hint: use 0 for first, and -1 for last single message"""
    try:
        if text:
            return Message.query.filter(Message.text == text)[number].time
        else:
            return Message.query.order_by(Message.id.desc()).limit(number).all()
    except (IndexError, OperationalError, InvalidRequestError) as e:
        return ['Error']


def store_direct(text):
    """ This will sstore a message directly to the database,
    bypassing the redis queue async workflow """
    try:
        entry = Message(text, datetime.now().replace(microsecond=0))
        db_session.add(entry)
        db_session.commit()
    except Exception:
        logging.error("Could not store message '%s', check your database settings." % text)


def check_env(env_name, value=None):
    """See if an environment variable is set"""
    try:
        os.environ[env_name]
    except KeyError:
        return False
    if value is None:
        return True
    elif value in os.environ[env_name]:
        return True
    else:
        return False


def tutorial_url(ref):
    return "{0}#{1}".format(
        "documentation/deploy/tutorials/deploy-demo-app.html",
        ref
    )


def checklist(url):
    """ This will return the status of each item in the
    demo app setup checklist """

    setup_status = []

    def check(desc, status, docpath):
        setup_status.append(Guidestep(desc, status, docpath))

    if "on-aptible.com" in url:
        endpoint_type = "Default"
    else:
        endpoint_type = "Custom"

    size = os.environ.get("APTIBLE_CONTAINER_SIZE")
    scaled = size is not None and int(size) != 1024

    try:
        read_messages('DB migration complete', 0)
        migrations = True
    except Exception:
        migrations = False

    check("Create an application", True, tutorial_url("create-an-app"))
    check("Deploy the application", True, tutorial_url("deploy-the-app"))
    check("Create an endpoint; current type: {0}".format(endpoint_type), True,
          tutorial_url("create-a-default-endpoint"))
    check("Configure the DATABASE_URL environment variable", check_env("DATABASE_URL"),
          tutorial_url("tell-the-application-about-your-databases"))
    check("Configure the REDIS_URL environment variable", check_env("REDIS_URL"),
          tutorial_url("tell-the-application-about-your-databases"))
    check("Run database migrations", migrations,
          tutorial_url("run-database-migrations"))
    check("Advanced: Application: scale your app up or down", scaled,
          "documentation/deploy/reference/apps/scaling.html#vertical-scaling")
    check("Advanced: Endpoints: force redirection to HTTPS", check_env("FORCE_SSL", "true"),
          "documentation/deploy/reference/apps/endpoints/https-endpoints/https-redirect.html")
    check("Advanced: Endpoints: change default timeout", check_env("IDLE_TIMEOUT"),
          "documentation/deploy/reference/apps/endpoints/timeouts.html#endpoint-timeouts")

    return setup_status


# Check if the database is initialized
try:
    logging.info("PostgreSQL database initialized at: %s",
                 read_messages('DB migration complete', 0))

    # Put a message in the database on startup
    store_direct("Web container started")

    # logging.debug some diagnostic info:
    logging.info("First web container started: %s",
                 read_messages('Web container started', 0))
    logging.info("Most recent web container started: %s",
                 read_messages('Web container started', -1))

except Exception:
    logging.error("PostgreSQL database is not initialized, did migrations run?")

# Log the completeness of the guide to the console on startup:
for step in checklist("UNAVAILABLE"):
    if step.status:
        completeness = "Completed"
    else:
        completeness = "Incomplete"

    if "Create an endpoint" in step.description:
        continue

    logging.info("%s : %s", step.description, completeness)


# Handle web requests
@app.route('/', methods=['GET', 'POST'])
def index():
    status = checklist(request.url)
    sum_complete = lambda total, s: total + 1 if s.status else total
    checklist_complete = reduce(sum_complete, status, 0)
    form = InputForm()
    if request.method == 'POST':
        try:
            # If the connection to Redis is set to use rediss://, but is connecting on an insecure port,
            # the connection just hangs at SSLSocket.do_handshake().
            # This signal/alarm will prevent the connection from hanging for more than 5 seconds. It will also
            # prevent any enqueue messages from taking more than 5 seconds, but the messages being enqueued
            # are small enough and happen in a small enough volume, that the alarm should never be an issue on
            # valid enqueue actions.
            signal.signal(signal.SIGALRM, timeout_alarm_handler)
            signal.alarm(5)
            queue.enqueue(store_message, form.message.data, datetime.now().replace(microsecond=0))
        except ConnectionError:
            return "ERROR: not queued, Redis cannot be reached. Check your settings", 500
        except TimeoutError:
            return "ERROR: not queued. Connection to Redis timed out. Check your REDIS_URL setting.", 500
        finally:
            # Connection was either successful or unsuccessful at this point. Either way,
            # the alarm is no longer needed, so turn it off.
            signal.alarm(0)
        return redirect('/')

    try:
        read_messages('DB migration complete', 0)
        return render_template('index.html', form=form, messages=read_messages('', 20),
                               checklist_complete=checklist_complete, checklist_len=len(status), status=status)
    except Exception:
        return render_template('index.html', form=form, checklist_complete=checklist_complete,
                               checklist_len=len(status), status=status)


def timeout_alarm_handler(_signum, _frame):
    raise TimeoutError


if __name__ == '__main__':
    app.run()
