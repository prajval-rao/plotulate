from imports import *

g_model = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")

class query_state(TypedDict):
    query_context: str
    file_context: list[dict[str, Any]]

graph = StateGraph(query_state)


def query_node(state: query_state):
    try:
        prompt = f"""You are a helpful AI assistant who answers user queries about a dataset. Keep your responses brief
        and do not use bold formatting. CONTEXTS TO GENERATE AN OPTIMAL ANSWER: USER QUERY: {state["query_context"]},
        DATASET: {state["file_context"]}"""
        response = g_model.invoke(prompt)
        return {"output": response}

    except:
        print("Error")






