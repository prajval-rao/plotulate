from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
from io import BytesIO
app = FastAPI()

def column_formatting(df):
    for column in df.columns:
        if df[column].dtype == "object":
            try:
                df[column] = pd.to_datetime(df[column].dropna())
            except:
                try:
                    df[column] = pd.to_numeric(df[column].dropna())
                except:
                    try:
                        df[column] = pd.to_timedelta(df[column].dropna())
                    except:
                        raise HTTPException(status_code=400, detail="Invalid column type for 1 or more columns")
    return df.columns
        
    

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
    return metadata
