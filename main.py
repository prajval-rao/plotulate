from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import RedirectResponse
import pandas as pd
import json
from io import BytesIO
app = FastAPI()

def column_formatting(df):
    for column in df.columns:
        if df[column].dtype == "object":
            try:
                df[column] = pd.to_datetime(df[column], errors="raise")
                continue
            except Exception:
                pass
            try:
                df[column] = pd.to_numeric(df[column], errors="raise")
                continue
            except Exception:
                pass
            try:
                df[column] = pd.to_timedelta(df[column], errors="raise")
                continue
            except Exception:
                pass            
    return {column: str(df[column].dtype) for column in df.columns}
        

@app.post("/upload")
async def input_data(file: UploadFile  = File(...)):
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Invalid file type")
    contents = await file.read()
    df = pd.read_excel(BytesIO(contents))
    metadata = {
        "filename": file.filename,
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "columns": column_formatting(df)
    }
    df.to_json("data.json", orient="records", indent=4, date_format="iso")
    return metadata








