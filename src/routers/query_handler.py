from src.routers.router_imports import *

load_dotenv() 

llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", temperature=0)


class QueryClassification(BaseModel):
    query_type: Literal["general", "sql", "visualise"] = Field(
        description=(
            "The type of query.\n"
            "general: the user wants to understand or ask about the data; nothing should change.\n"
            "sql: the user wants to change the database.\n"
            "visualise: the user wants a chart based on the data."
        )
    )


class State(MessagesState):
    query_type: str
    result: str


classifier = llm.with_structured_output(QueryClassification)


def classify(state: State):
    out = classifier.invoke(state["messages"])
    return {"query_type": out.query_type}


def route(state: State):
    return state["query_type"]


def general_node(state: State):
    return {"result": "general"}

def sql_node(state: State):
    return {"result": "sql"}

def visualise_node(state: State):
    return {"result": "visualise"}


graph = StateGraph(State)
graph.add_node("classify", classify)
graph.add_node("general", general_node)
graph.add_node("sql", sql_node)
graph.add_node("visualise", visualise_node)

graph.add_edge(START, "classify")
graph.add_conditional_edges(
    "classify",
    route,
    {"general": "general", "sql": "sql", "visualise": "visualise"},
)
for n in ("general", "sql", "visualise"):
    graph.add_edge(n, END)

app = graph.compile()

ask = {"messages": [("user", "Insert two random values in each column")]}
for step in app.stream(ask):
    print("Step output:", step)
    print("-" * 40)