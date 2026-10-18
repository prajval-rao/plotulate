from imports import *
import datetime

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/submit")
async def format_file(file: UploadFile = File(...)):
    if not file.filename.endswith(("xlsx", "xls")):
        raise HTTPException(status_code=400, detail="Upload file of correct type. ")
    contents = await file.read()
    try:
        df = pd.read_excel(io.BytesIO(contents))
        df = df.fillna(0)
        # axis = 0 is for rows
        df = df.dropna(axis = 0)
        for column in df.columns:
            s = df[column]
            if pd.api.types.is_datetime64_any_dtype(s):
                df[column] = s.dt.strftime('%Y-%m-%d %H:%M:%S')
            elif s.dtype == object:
                non_null = s.dropna()
                if non_null.empty:
                    continue
                # check all values, not just the first, since Excel columns can be mixed
                if non_null.map(lambda x: isinstance(x, (datetime.datetime, datetime.date))).all():
                    df[column] = s.map(
                        lambda x: x.strftime('%Y-%m-%d %H:%M:%S') if pd.notna(x) else None
                    )
            df[column] = pd.to_numeric(df[column], errors="coerce").fillna(df[column])
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Excel file failed to load: {e}")
    return {'filename': file.filename, 'content': df.to_dict(orient="records")}


