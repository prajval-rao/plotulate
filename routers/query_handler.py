from imports import *   # error to be resolved
from typing import Literal
from pydantic import Field

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
query_type_model = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", temperature=0.7)


class QueryClassification(BaseModel):
    query_type: Literal["general", "sql", "visualise"] = Field("""The type of query.\n"
    general: the user wants to understand or ask about the data, and nothing should change. NO SELECT operation or filtering either. \n
    sql: the user wants to change the database.
    visualise: the user wants a chart based on the data.""")

class ResultState(TypedDict):
    result: str

query_node = query_type_model.with_structured_output(QueryClassification)

def node1(state: ResultState):
    return {"result": "general"}

def node2(state: ResultState):
    return {"result": "sql"}

def node3(state: ResultState):
    return {"result": "visualise"}

graph = StateGraph(MessagesState)
graph.add_node(query_node)
graph.add_node(node1)
graph.add_node(node2)
graph.add_node(node3)

graph.add_edge(START, query_node)
graph.add_conditional_edges(query_node, query_node.query_type, {"general": node1, "sql": node2, "visualise": node3})

app = graph.compile()
ask = {"messages": [("user", "What is this dataset about?")]}
for step in app.stream(ask):
  print("Step output:", step)
  print("-" * 40)
