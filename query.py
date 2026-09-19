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

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
g_model = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", temperature=0.7)

class QueryState(TypedDict):
    current_query: str
    query_context: list[str]
    file_context: Any

class QueryTemplate(BaseModel):
    query: str
    session_id: str
    file_content: Any

graph = StateGraph(QueryState)

session_storage: dict[str, QueryState] = {}

@query_app.post("/generate_response")
async def query_node(payload: QueryTemplate):
    try:
        if payload.session_id not in session_storage:
            session_storage[payload.session_id] = {"current_query": "", "query_context": [], "file_context": None}
        elif payload.file_content != session_storage[payload.session_id]["file_context"]:
            session_storage[payload.session_id] = {"current_query": "", "query_context": [], "file_context": None}
        else:
            pass
        session_storage[payload.session_id]["query"] = payload.query
        session_storage[payload.session_id]["query_context"].append(payload.query)
        session_storage[payload.session_id]["file_context"] = payload.file_content

        state = session_storage[payload.session_id] 
        prompt = f"""You are a helpful AI assistant who answers user queries about a dataset. 
        Keep your responses brief and do not use bold formatting. 
        Prioritise the current query when generating a response unless the history is highly relevant. 
        CONTEXTS TO GENERATE AN OPTIMAL ANSWER: 
        CURRENT QUERY BEING ASKED: {state["current_query"]}, 
        USER QUERY HISTORY: {state["query_context"]},
        DATASET: {state["file_context"]}
        If you find something to be too irrelevant from the dataset then do not answer and instead bring the user back
        to discussing the dataset. """

        response = g_model.invoke(prompt)
        print({"output": response.content[0]['text']})
        return {"output": response.content[0]['text']}
    
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}






