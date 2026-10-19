from imports import *
from fastapi.concurrency import run_in_threadpool
import datetime
import uuid
import re
from database import models
from database import database_create

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def df_to_records(df: pd.DataFrame):
    return df.astype(object).where(df.notna(), None).to_dict(orient="records")

def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna(how="all")                     
    df.columns = [str(c) for c in df.columns]
    if df.columns.duplicated().any():
        raise ValueError("Duplicate column names")

    for col in df.columns:
        s = df[col]
        if s.dtype != object:
            continue
        non_null = s.dropna()
        if non_null.empty:
            continue
        if non_null.map(lambda x: isinstance(x, (datetime.datetime, datetime.date))).all():
            df[col] = pd.to_datetime(s)
        else:
            num = pd.to_numeric(s, errors="coerce")
            if num.notna().sum() == s.notna().sum():   # every non-null value converted
                df[col] = num
    return df

@router.post("/submit")
async def format_file(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Upload file of correct type. ")
    contents = await file.read()
    try:
        df = await run_in_threadpool(lambda: clean_df(pd.read_excel(io.BytesIO(contents))))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Excel file failed to load and format: {e}")
    table_name = f"U1_{uuid.uuid4().hex[:12]}"
    try:
        models.fetch_PandasData(df, table_name=table_name, base_class=database_create.Base)
        database_create.Base.metadata.create_all(database_create.engine)
        await run_in_threadpool(
            lambda: df.to_sql(table_name, database_create.engine, if_exists="append", index=False)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save data: {e}")
    
    return {'filename': file.filename, 
            'table_name': table_name,
            'content': df_to_records(df)}


@router.get("/data/{table_name}")
def get_data(table_name: str, limit: int = 100):
    if not re.fullmatch(r"U1_[0-9a-f]{12}", table_name):
        raise HTTPException(status_code=404, detail=f"Unknown dataset")
    try:
        df = pd.read_sql_table(table_name, database_create.engine).head(limit)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Unknown dataset")
    return {'table_name': table_name, 'content': df_to_records(df)}
