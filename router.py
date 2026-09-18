from imports import *
from main import app
from query import query_app

root_app = FastAPI()

origins = ["http://127.0.0.1:5500", "http://localhost:3000"]

root_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

root_app.mount("/query", query_app)
root_app.mount("/", app)