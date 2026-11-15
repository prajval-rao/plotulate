from imports import *
import httpx
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
# file created automatically

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}, # sqlite-specific, only allows one thread so we disable the restriction here
    echo = True
)

# factory that creates database sessions, session is a transaction:
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)  # to control changes made

class Base(DeclarativeBase):
    pass

def get_db():
    with SessionLocal() as db:
        yield db








