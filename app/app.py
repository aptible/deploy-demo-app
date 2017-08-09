import logging
import os

from datetime import datetime
from flask import Flask, redirect, request, render_template
from flask_wtf import FlaskForm
from functools import reduce
from psycopg2 import OperationalError
from redis.exceptions import ConnectionError
from rq import Queue
from sqlalchemy.exc import InvalidRequestError
from wtforms import TextField, SubmitField
# from wtforms import validators, ValidationError

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
db_init = False


@app.teardown_appcontext
def shutdown_session(exception=None):
    """ Remove sessions at end of request """
    db_session.remove()


class InputForm(FlaskForm):
    """ This form is used to submit information from a webpage """
    message = TextField("Your message")
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


def check_env(envname, value=None):
    """See if an environment variable is set"""
    try:
        os.environ[envname]
    except KeyError:
        return False
    if value is  None:
        return True
    elif value in os.environ[envname]:
        return True
    else:
        return False


def checklist(migrations, url):
    """ This will return the status of each item in the
    demo app setup checklist """

    setup_status = []

    def check(desc,status,docpath):
        setup_status.append(Guidestep(desc,status,docpath))

    if "on-aptible.com" in url:
        endpointtype = "Default"
    else:
        endpointtype = "Custom"

    if check_env("APTIBLE_CONTAINER_SIZE") and \
       (os.environ["APTIBLE_CONTAINER_SIZE"] != "1024"):
        scaled = True
    else:
        scaled = False

    check("Create an application", True,
          "documentation/nclave/tutorials/demo-app.html#create-an-application")
    check("Deploy the application", True,
          "documentation/enclave/tutorials/demo-app.html#deploy-the-application")
    check("Create an endpoint; current type: "+endpointtype, True,
          "documentation/nclave/tutorials/demo-app.html#create-a-default-endpoint")
    check("Configure the DATABASE_URL environment variable", check_env("DATABASE_URL"),
          "documentation/enclave/tutorials/demo-app.html#tell-your-application-about-the-databases")
    check("Configure the REDIS_URL environment variable", check_env("REDIS_URL"),
          "documentation/enclave/tutorials/demo-app.html#tell-your-application-about-the-databases")
    check("Run database migrations", migrations,
          "documentation/enclave/tutorials/demo-app.html#run-database-migrations")
    # check("Automate database migrations", False,
    #       "enclave/tutorials/faq/database-migrations.html#automating-database-migrations")
    check("Advanced: Application: scale your app up or down", scaled,
          "documentation/enclave/reference/apps/scaling.html#vertical-scaling")
    check("Advanced: Endpoints: force redirection to HTTPS", check_env("FORCE_SSL","True"),
          "documentation/enclave/reference/apps/endpoints/https-endpoints/https-redirect.html")
    check("Advanced: Endpoints: change default timeout", check_env("IDLE_TIMEOUT"),
          "documentation/enclave/reference/apps/endpoints/timeouts.html#endpoint-timeouts")

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
    db_init = True

except Exception:
    db_init = False
    logging.error("PostgreSQL database is not initialized, did migrations run?")

# Log the completeness of the guide to the console on startup:
for step in checklist(db_init, "UNAVAILABLE"):
    if step.status:
        completeness = "Completed"
    else:
        completeness = "Incompete"

    if "Create an endpoint" in step.description:
        continue

    logging.info("%s : %s", step.description, completeness)


# Handle web requests
@app.route('/', methods=['GET', 'POST'])
def index():
    status = checklist(db_init, request.url)
    sum_complete = lambda total,s: total + 1 if (s.status) else total
    checklist_complete = reduce(sum_complete,status,0)
    form = InputForm()
    if request.method == 'POST':
        try:
            queue.enqueue(store_message, form.message.data, datetime.now().replace(microsecond=0))
        except ConnectionError:
            return "ERROR: not queued, Redis cannot be reached. Check your settings", 500
        return redirect('/')

    if db_init:
        return render_template('index.html', form=form, messages=read_messages('', 20), checklist_complete=checklist_complete, checklist_len=len(status), status=status)
    else:
        return render_template('index.html', form=form, checklist_complete=checklist_complete, checklist_len=len(status), status=status)

if __name__ == '__main__':

    app.run()
