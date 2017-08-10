from sqlalchemy import Column, Integer, String, DateTime, func
from databases import Base


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    text = Column(String(150), unique=False)
    time = Column(DateTime, default=func.now())

    def __init__(self, text=None, time=None):
        self.text = text
        self.time = time

    def __repr__(self):
        return '<Message %r>' % (self.text)


class Guidestep:
    def __init__(self, description, status, docpath):
        self.description = description
        self.status = status
        self.docpath = docpath
