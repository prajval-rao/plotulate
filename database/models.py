from imports import *
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class userData(Base):
    __tablename__ = "userdata1"
    id: Mapped[int] = mapped_column(primary_key = True) # implicitly converts Python datatype to SQL datatype