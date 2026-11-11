from imports import *
from typing import Optional

router = APIRouter()
queryspec_router = APIRouter()

router.include_router(queryspec_router)
templates = Jinja2Templates(directory="templates")

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
g_model = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", temperature=0.7)

class QueryState(TypedDict):
    current_query: str
    query_context: list[str]
    file_context: Any
    table_name: str

class QueryPayload(BaseModel):
    query: str
    session_id: str
    file_content: Any
    query_class: Optional[str] = None
    table_name: Optional[str] = None

graph = StateGraph(QueryState)

session_storage: dict[str, QueryState] = {}



async def run_sql_query(query: str, table_name: str):

    prompt = f"""You are an assistant that converts a user request into a single SQL statement.
    Table: {table_name}
    Dataset sample: FILE CONTENTS HERE!!!
    Request: {query}
    Return only the SQL."""

@router.post("/generate_response")
async def query_node(payload: QueryPayload):
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
        session_storage[payload.session_id]["table_name"] = payload.table_name
        try:
            #if payload.query_class == "general":
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

            #elif payload.query_class == "sql":
            #    sql_response = None
        
        except Exception as e:
            print(f"Error (calling LLM): {e}")
            return {"error": str(e)}
        
    except Exception as e:
        print(f"Error (query storage): {e}")
        return {"error": str(e)}









