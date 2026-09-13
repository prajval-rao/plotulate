from imports import *

app = FastAPI()
templates = Jinja2Templates(directory="templates")

origins = ["http://127.0.0.1:5500", "http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/submit")
async def format_file(file: UploadFile = File(...)):
    if not file.filename.endswith(("xlsx", "xls")):
        raise HTTPException(status_code=400, detail="Upload file of correct type. ")
    contents = await file.read()

    try:
        df = pd.read_excel(io.BytesIO(contents))
        df = df.fillna(0)
        for column in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[column]):
                df[column] = df[column].dt.strftime('%Y-%m-%d %H:%M:%S')
                continue
            if df[column].dtype == "object":
                try:
                    df[column] = pd.to_datetime(df[column], errors="raise", format="%Y-%m-%d")
                    continue
                except (ValueError, TypeError):
                    pass
            df[column] = pd.to_numeric(df[column], errors="coerce").fillna(df[column])
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Excel file failed to load: {e}")
    return {'filename': file.filename, 'content': df.to_dict(orient="records")}

