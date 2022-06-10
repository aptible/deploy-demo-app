from datetime import datetime
import logging
import sys
import traceback

from databases import init_db, db_session
from models import Message

logging.basicConfig(level=logging.DEBUG)

logging.info("Attempting DB initialization...")

try:
    init_db()
    m = Message("DB migration complete",
                datetime.now().replace(microsecond=0))
    db_session.add(m)
    db_session.commit()
    db_session.remove()
    logging.info("Done!")
except Exception:
    traceback.print_exc(file=sys.stderr)
    logging.error("DB initialization failed, verify the DATABASE_URL setting.")
