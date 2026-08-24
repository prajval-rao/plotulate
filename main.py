from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import RedirectResponse
import io
import pandas as pd
import openpyxl
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["http://127.0.0.1:5500/", "http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def home():
    return RedirectResponse(url="/upload")

@app.get("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(("xlsx", "xls")):
        raise HTTPException(status_code=400, detail="Upload file of correct type. ")
    contents = await file.read()

    try:
        df = pd.read_excel(io.BytesIO.read(contents))
        df.fillna(0)
        for column in df:
            try:
                df[column] = df[column].astype("int64")
                continue
            except:
                pass
            try:
                df[column] = df[column].astype("float64")
                continue
            except:
                pass
            try:
                df[column] = df[column].astype("datetime64[ns]")
            except:
                raise HTTPException(status_code=400, detail="One or more columns are of an unsupported datatype. ")
    except:
        raise HTTPException(status_code=400, detail="Excel file failed to load. ")
    return {'filename': file.filename, 'content': df.to_json(orient="table")}






