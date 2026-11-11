from sqlalchemy import MetaData, Table
from sqlalchemy.orm import Session
import human_to_schema

def sql_query(query: str, table_name: str, db: Session):
    t = Table(table_name, MetaData(), autoload_with=db.get_bind())
    schema_spec = human_to_schema.human_to_query_spec(query, table_name)
    dim = schema_spec.dimensions
    for col in dim:
        print(col)

print(sql_query("I want to see the data of all the people who got an average calculation of more than 13", "U1_034585f91fc2"))