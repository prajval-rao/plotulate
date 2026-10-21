from imports import *
from typing import Literal
from pydantic import Field

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
query_type_model = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", temperature=0.7)


class QueryClassification(BaseModel):
    query_type: Literal["general", "sql", "visualise"] = Field("""The type of query.\n"
    General: the user wants to understand or ask about the data, and nothing should change. NO SELECT operation or filtering either. \n
    SQL: the user wants to change the database.
    VISUALISE: the user wants a chart.""")

query_node = query_type_model.with_structured_output(QueryClassification)

graph = StateGraph(MessagesState)
graph.add_node(query_node)
graph.add_edge(START, query_node)


