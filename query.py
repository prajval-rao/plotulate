from imports import *

query_app = FastAPI()
templates = Jinja2Templates(directory="templates")

origins = ["http://127.0.0.1:5500", "http://localhost:3000"]

query_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

g_model = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")

class QueryState(TypedDict):
    query_context: str
    file_context: list[dict[str, Any]]

graph = StateGraph(QueryState)

@query_app.post("/generate_response")
async def query_node(state: QueryState):
    try:
        prompt = f"""You are a helpful AI assistant who answers user queries about a dataset. Keep your responses brief
        and do not use bold formatting. CONTEXTS TO GENERATE AN OPTIMAL ANSWER: USER QUERY: {state["query_context"]},
        DATASET: {state["file_context"]}"""
        response = g_model.invoke(prompt)
        return {"output": response}
    
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}






