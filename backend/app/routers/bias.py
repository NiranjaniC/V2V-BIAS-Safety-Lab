from fastapi import APIRouter, HTTPException
import pandas as pd
from pathlib import Path
import numpy as np

router = APIRouter()


BASE_PATH = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_PATH / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)


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


@router.get("/status")
def bias_status():
    return {"module": "Bias Detection", "status": "OK"}



@router.get("/overview/{filename}")
def bias_overview(filename: str):
    file_path = RAW_DIR / filename
    if not file_path.exists():
        raise HTTPException(404, "File not found")

    df = load_dataframe(file_path)
    df = df.fillna("")

    missing_rate = df.isna().sum().sum() / (df.shape[0] * df.shape[1])
    skewness = df.select_dtypes(include=["float", "int"]).skew().abs().mean()

    # Bias score (0–100)
    bias_score = round((missing_rate * 40) + (skewness * 60), 2)
    bias_score = min(bias_score, 100)

    return {
        "filename": filename,
        "rows": df.shape[0],
        "columns": list(df.columns),
        "missing_value_rate": round(missing_rate, 4),
        "avg_skewness": round(skewness, 4),
        "bias_score": bias_score
    }


# -------------------------------------------------------
# CLASS IMBALANCE
# -------------------------------------------------------
@router.get("/imbalance/{filename}")
def class_imbalance(filename: str, target: str = "collision_risk"):

    file_path = RAW_DIR / filename
    if not file_path.exists():
        raise HTTPException(404, "File not found")

    df = load_dataframe(file_path)

    if target not in df.columns:
        raise HTTPException(400, f"Target column '{target}' not found")

    counts = df[target].value_counts().to_dict()
    total = sum(counts.values())

    imbalance = {
        label: round((count / total) * 100, 2)
        for label, count in counts.items()
    }

    return {
        "target_column": target,
        "distribution_percent": imbalance,
        "recommendation": "Balance dataset using oversampling/undersampling if any class <10%."
    }


# -------------------------------------------------------
# MISSING VALUES BIAS
# -------------------------------------------------------
@router.get("/missing/{filename}")
def missing_bias(filename: str):
    file_path = RAW_DIR / filename
    if not file_path.exists():
        raise HTTPException(404, "File not found")

    df = load_dataframe(file_path)
    missing = df.isna().sum().to_dict()

    return {
        "filename": filename,
        "missing_by_column": missing,
        "columns_with_missing": [c for c, v in missing.items() if v > 0]
    }


# -------------------------------------------------------
# NUMERIC BIAS
# -------------------------------------------------------
@router.get("/numeric/{filename}")
def numeric_bias(filename: str):
    file_path = RAW_DIR / filename
    if not file_path.exists():
        raise HTTPException(404, "File not found")

    df = load_dataframe(file_path)
    numeric_df = df.select_dtypes(include=["int", "float"])

    if numeric_df.empty:
        raise HTTPException(400, "No numeric features present")

    skew = numeric_df.skew().to_dict()

    # Handle std = 0 case (avoid divide-by-zero)
    outlier_counts = {}
    for col in numeric_df.columns:
        col_std = numeric_df[col].std()
        if col_std == 0:
            outlier_counts[col] = 0
        else:
            outlier_counts[col] = int(
                ((numeric_df[col] - numeric_df[col].mean()).abs() > 3 * col_std).sum()
            )

    return {
        "numeric_columns": list(numeric_df.columns),
        "skewness": skew,
        "outliers_per_column": outlier_counts
    }
