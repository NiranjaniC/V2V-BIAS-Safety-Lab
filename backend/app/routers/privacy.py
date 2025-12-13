import re
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
# PII PATTERNS
# ---------------------------------------
PII_PATTERNS = {
    "email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "phone": r"\b(?:\+?\d{1,3})?[ -]?\d{10}\b",
    "aadhaar": r"\b\d{4}\s?\d{4}\s?\d{4}\b",
    "pan": r"[A-Z]{5}[0-9]{4}[A-Z]{1}",
}


def scan_text(text: str):
    """Scan a string and return PII matches."""
    results = {}
    for pii, pattern in PII_PATTERNS.items():
        matches = re.findall(pattern, text)
        if matches:
            results[pii] = matches
    return results


def process_privacy_audit(file: UploadFile):
    """Run privacy audit logic."""
    file_path = RAW_DIR / file.filename

    # Save uploaded file
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    df = pd.read_csv(file_path)
    df = df.fillna("")

    pii_results = {}
    total_hits = 0

    for col in df.columns:
        text_data = " ".join(df[col].astype(str).tolist())
        matches = scan_text(text_data)

        if matches:
            pii_results[col] = matches
            total_hits += sum(len(v) for v in matches.values())

    # Risk scoring
    if total_hits == 0:
        risk = "Low"
    elif total_hits < 5:
        risk = "Medium"
    else:
        risk = "High"

    # Recommendations
    recommendations = []
    if "email" in str(pii_results):
        recommendations.append("Remove or mask email addresses.")
    if "phone" in str(pii_results):
        recommendations.append("Remove or hash phone numbers.")
    if "aadhaar" in str(pii_results):
        recommendations.append("Never store Aadhaar numbers directly.")
    if "pan" in str(pii_results):
        recommendations.append("Mask PAN numbers (e.g., XXXXX1234X).")

    return {
        "filename": file.filename,
        "pii_detected": pii_results,
        "total_hits": total_hits,
        "risk_level": risk,
        "recommendations": recommendations,
    }


# ---------------------------------------
# API ROUTES (THIS WAS MISSING)
# ---------------------------------------

@router.get("/status")
def privacy_status():
    return {"module": "Privacy Audit", "status": "OK"}


@router.post("/audit")
async def audit_file(file: UploadFile):
    if not file.filename.endswith(".csv"):
        raise HTTPException(400, "Only CSV files are supported")
    return process_privacy_audit(file)
