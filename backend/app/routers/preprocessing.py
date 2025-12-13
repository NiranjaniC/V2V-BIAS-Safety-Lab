from fastapi import APIRouter, HTTPException
import pandas as pd
import os
from pathlib import Path

router = APIRouter()

RAW_DIR = Path("backend/app/data/raw")           # folder where uploads go
PROCESSED_DIR = Path("processed_files")       # new folder for output

RAW_DIR.mkdir(exist_ok=True)
PROCESSED_DIR.mkdir(exist_ok=True)


@router.get("/status")
def preprocessing_status():
    return {"module": "Preprocessing", "status": "OK"}


@router.get("/preview/{filename}")
def preview_file(filename: str):
    file_path = RAW_DIR / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    try:
        df = load_dataframe(file_path)
        return {
            "filename": filename,
            "columns": list(df.columns),
            "rows": len(df),
            "sample_data": df.head(5).to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/summary/{filename}")
def summary_file(filename: str):
    file_path = RAW_DIR / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    try:
        df = load_dataframe(file_path)
        return {
            "rows": df.shape[0],
            "columns": df.shape[1],
            "missing_values": df.isnull().sum().to_dict(),
            "column_types": df.dtypes.apply(lambda x: str(x)).to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/clean/{filename}")
def clean_file(filename: str):
    file_path = RAW_DIR / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File does not exist")

    try:
        df = load_dataframe(file_path)

        cleaned_df = df.dropna().drop_duplicates()

        output_path = PROCESSED_DIR / f"cleaned_{filename}"
        save_dataframe(cleaned_df, output_path)

        return {
            "message": "File cleaned successfully",
            "saved_as": output_path.name,
            "rows_before": len(df),
            "rows_after": len(cleaned_df)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.post("/convert/csv/{filename}")
def convert_to_csv(filename: str):
    file_path = RAW_DIR / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    try:
        df = load_dataframe(file_path)

        output_name = filename.split('.')[0] + ".csv"
        output_path = PROCESSED_DIR / output_name

        df.to_csv(output_path, index=False)

        return {"message": "Converted to CSV", "saved_as": output_name}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



def load_dataframe(file_path: Path):
    ext = file_path.suffix.lower()

    if ext == ".csv":
        return pd.read_csv(file_path)
    elif ext in [".xlsx", ".xls"]:
        return pd.read_excel(file_path)
    elif ext == ".json":
        return pd.read_json(file_path)
    else:
        raise ValueError("Unsupported file format")


def save_dataframe(df, path: Path):
    ext = path.suffix.lower()

    if ext == ".csv":
        df.to_csv(path, index=False)
    elif ext in [".xlsx", ".xls"]:
        df.to_excel(path, index=False)
    elif ext == ".json":
        df.to_json(path, orient="records")
    else:
        raise ValueError("Unsupported file format for saving")
