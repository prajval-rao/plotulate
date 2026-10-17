from imports import *
import httpx
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_app = FastAPI()
origins = ["http://127.0.0.1:5500", "http://localhost:3000"]
db_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




