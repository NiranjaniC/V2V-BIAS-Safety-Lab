import pandas as pd
from pathlib import Path
from fastapi import UploadFile, APIRouter, HTTPException

router = APIRouter()

# ---------------------------------------
# FIXED BASE PATH
# ---------------------------------------
BASE_PATH = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_PATH / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------
# UPLOAD FILE
# ---------------------------------------
@router.post("/upload")
async def upload_file(file: UploadFile):
    if not file.filename.endswith(".csv"):
        raise HTTPException(400, "Only CSV files allowed")

    file_path = RAW_DIR / file.filename

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return {"message": "File uploaded successfully"}


# ---------------------------------------
# LIST FILES
# ---------------------------------------
@router.get("/files")
async def list_files():
    files = [f.name for f in RAW_DIR.glob("*.csv")]
    return {"files": files}


# ---------------------------------------
# PREVIEW FILE (Fix for your error)
# ---------------------------------------
@router.get("/preview/{filename}")
async def preview_file(filename: str):
    file_path = RAW_DIR / filename

    if not file_path.exists():
        raise HTTPException(404, "File not found")

    try:
        df = pd.read_csv(file_path)

        preview_data = df.head(10).to_dict(orient="records")

        return {
            "filename": filename,
            "preview": preview_data
        }

    except Exception as e:
        raise HTTPException(500, f"Error reading file: {str(e)}")
