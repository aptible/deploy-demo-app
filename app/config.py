import os
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False
TESTING = False
CSRF_ENABLED = True
SECRET_KEY = 'gobbledygook'

try:
    DATABASE_URL = os.environ['DATABASE_URL']
except KeyError:
    DATABASE_URL = "postgresql://localhost:5432/db"

try:
    REDIS_URL = os.environ['REDIS_URL']
except KeyError:
    REDIS_URL = "redis://localhost:5432/db"
