from fastapi import HTTPException
from sqlalchemy import inspect
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine, Inspector
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from ..database import database_create
from src.routers.sql_query_schema import QuerySpec

load_dotenv()
g_model = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", temperature=0)

def fetch_table(insp: Inspector, table_name: str) -> str:
    if table_name not in insp.get_table_names():
        raise HTTPException(404, f"Unknown table: {table_name}")
    return table_name

template = ChatPromptTemplate.from_messages(
    [
        ("system", "Convert the request into a QuerySpec. Use ONLY these columns:\n{schema}"), # datetime support
        ("human", "{query}"),
    ]
)

chain = template | g_model.with_structured_output(QuerySpec)

def describe_schema(table_name: str, bind: Engine = database_create.engine) -> str:
    insp = inspect(bind) # read database
    lines = []
    table_name = fetch_table(insp, table_name)
    cols = ", ".join(f"{c['name']} ({c['type']})" for c in insp.get_columns(table_name))
    lines.append(f"{table_name}: {cols}")
    return "\n".join(lines)

def human_to_query_spec(query: str, table_name: str):
    sql_query_spec = chain.invoke({"schema": describe_schema(table_name), "query": query})
    return sql_query_spec

print(human_to_query_spec("I want to see the branch column only", "U1_034585f91fc2"))



