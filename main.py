from imports import *
from routers import router

app = FastAPI()

origins = ["http://127.0.0.1:5500", "http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)