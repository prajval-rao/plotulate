from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, MessagesState, START, END
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from typing import Literal