from imports import *
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class userData(Base):
    __tablename__ = "userdata1"