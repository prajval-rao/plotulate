from imports import *
from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

def fetch_PandasData(df: pd.DataFrame, base_class = Base):
    type_mapping = {
        'int64': Integer,
        'int32': Integer,
        'float64': Float,
        'float32': Float,
        'object': String,
        'string': String,
        'bool': Boolean,
        'datetime64[ns]': DateTime,
    }

    attributes = {
        '__tablename__' : "randomname" # change when multiple users feature implemented
    }
    attributes['id': Mapped(int)] = mapped_column(primary_key = True)
    for col_name, dtype in df.dtypes.items():
        if col_name == 'id':
            continue
        col_type = type_mapping.get(dtype, str)
        attributes[str(col_name): Mapped(col_type)] = mapped_column()
    return type("UserData1", (base_class,), attributes)
        



class userData(Base):
    __tablename__ = "userdata1"
    id: Mapped[int] = mapped_column(primary_key = True) # implicitly converts Python datatype to SQL datatype

