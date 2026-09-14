from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import RedirectResponse
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.types import interrupt
import io
import pandas as pd
import openpyxl
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
import python_multipart
from typing import TypedDict, Any
from langgraph.checkpoint.memory import MemorySaver
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, MessagesState, START, END
