from imports import *
from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from .database_create import Base, engine

def fetch_PandasData(df: pd.DataFrame, table_name: str, base_class = Base):
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
        '__tablename__' : table_name, # change when multiple users feature implemented
        "__table_args__": {"extend_existing": True}, # allows re-declaring the same table
        "id": mapped_column(Integer, primary_key = True)
    }
    for col_name, dtype in df.dtypes.items():
        if col_name == 'id':
            continue
        col_type = type_mapping.get(str(dtype), String)
        attributes[str(col_name)] = mapped_column(col_type)
    return type("UserData1", (base_class,), attributes)
        



