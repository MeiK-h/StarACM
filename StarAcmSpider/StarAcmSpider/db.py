from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///memory')

Base = declarative_base()


def create_table():
    Base.metadata.create_all(engine)


def get_session():
    Session = sessionmaker(bind=engine)
    return Session()
