from sqlalchemy import (
    create_engine,
)
from sqlalchemy.orm import(
    DeclarativeBase,
    sessionmaker,
    Session
)

class Base(DeclarativeBase):  pass

engine = create_engine('sqlite:///database.db', echo=True, connect_args = {'check_same_thread': False})
SessionLocale = sessionmaker(bind=engine)


def get_db():
    session = SessionLocale()
    try:
        yield session
    finally:
        session.close()