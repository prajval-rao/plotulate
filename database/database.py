from imports import *
import httpx
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# file created automatically
SQLALCHEMY_DATABASE_URL = "sqlite:///./userdata.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}, # sqlite-specific, only allows one thread so we disable the restriction here
)

# factory that creates database sessions, session is a transaction:
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)  # to control changes made

class Base(DeclarativeBase):
    pass

def get_db():
    with SessionLocal() as db:
        yield db








