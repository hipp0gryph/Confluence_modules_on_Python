from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import conf

Base = declarative_base()

engine = create_engine(conf.URL)


def init():
    Base.metadata.create_all(engine)


def get_session():
    return Session(bind=engine)
