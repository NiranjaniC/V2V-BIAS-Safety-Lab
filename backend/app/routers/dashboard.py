# backend/app/routers/dashboard.py
from fastapi import APIRouter, HTTPException
import pandas as pd
import os
from pathlib import Path
from typing import Any, Dict, List

router = APIRouter()


BASE_DIR_PRIMARY = Path("backend") / "app" / "data" / "raw"
BASE_DIR_FALLBACK = Path("backend") / "app" / "data"

BASE_DIR_PRIMARY.mkdir(parents=True, exist_ok=True)
BASE_DIR_FALLBACK.mkdir(parents=True, exist_ok=True)



def _to_native(value: Any) -> Any:
    try:
        
        if hasattr(value, "item"):
            return value.item()
        # typical python numeric
        if isinstance(value, (int, float, str, bool)):
            return value
    except Exception:
        pass
    # fallback: try cast to float/int/str
    try:
        return float(value)
    except Exception:
        try:
            return int(value)
        except Exception:
            return str(value)


def _series_counts_to_dict(s: pd.Series) -> Dict[str, int]:
    """
    Convert a value_counts Series into a plain dict with native ints.
    """
    d = {}
    for k, v in s.items():
        key = str(k)
        d[key] = int(v) if hasattr(v, "__int__") else _to_native(v)
    return d


def _describe_to_native(d: pd.Series) -> Dict[str, Any]:
    """
    Convert pandas describe() series to native types.
    """
    out = {}
    for k, v in d.items():
        out[str(k)] = _to_native(v)
    return out


def _find_file_path(filename: str) -> Path:
    """
    Search primary then fallback directories. Raise 404 if not present.
    """
    p1 = BASE_DIR_PRIMARY / filename
    p2 = BASE_DIR_FALLBACK / filename

    if p1.exists():
        return p1
    if p2.exists():
        return p2

    raise HTTPException(status_code=404, detail=f"File '{filename}' not found in data folders")


def load_file(filename: str) -> pd.DataFrame:
    """
    Load CSV / Excel / JSON and return pandas DataFrame.
    """
    file_path = _find_file_path(filename)
    ext = file_path.suffix.lower().lstrip(".")

    try:
        if ext == "csv":
            return pd.read_csv(file_path)
        elif ext in ("xlsx", "xls"):
            return pd.read_excel(file_path)
        elif ext == "json":
            return pd.read_json(file_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read file: {e}")


def _get_best_column(df: pd.DataFrame, candidates: List[str]) -> str:
    """
    Return the first column from candidates that exists in df (case-insensitive).
    """
    lowered = {c.lower(): c for c in df.columns}
    for cand in candidates:
        if cand.lower() in lowered:
            return lowered[cand.lower()]
    return None

@router.get("/status")
def dashboard_status():
    return {"module": "Dashboard", "status": "OK"}


@router.get("/summary/{filename}")
def dashboard_summary(filename: str):
    df = load_file(filename)

    summary = {
        "total_records": int(len(df)),
        "columns": list(df.columns),
        "missing_values": {str(k): int(v) for k, v in df.isnull().sum().items()},
        "dtypes": {str(k): str(v) for k, v in df.dtypes.items()},
    }

    return summary


@router.get("/speed-stats/{filename}")
def speed_stats(filename: str):
    df = load_file(filename)

    
    col = _get_best_column(df, ["speed_kmh", "speed", "vehicle_speed"])
    if not col:
        raise HTTPException(status_code=400, detail="Column 'speed_kmh' (or alias) not found")

    
    df[col] = pd.to_numeric(df[col], errors="coerce")
    df_clean = df[col].dropna()
    if df_clean.empty:
        raise HTTPException(status_code=400, detail=f"No numeric values found in '{col}'")

    stats = {
        "col": col,
        "min_speed": _to_native(df_clean.min()),
        "max_speed": _to_native(df_clean.max()),
        "avg_speed": _to_native(df_clean.mean()),
        "median_speed": _to_native(df_clean.median()),
        "std_speed": _to_native(df_clean.std()),
        "count": int(df_clean.count()),
        "describe": _describe_to_native(df_clean.describe())
    }

    return stats


@router.get("/vehicle-distribution/{filename}")
def vehicle_distribution(filename: str):
    df = load_file(filename)

    col = _get_best_column(df, ["vehicle_type", "veh_type"])
    if not col:
        raise HTTPException(status_code=400, detail="Column 'vehicle_type' not found")

    dist = _series_counts_to_dict(df[col].value_counts())
    return {"vehicle_distribution": dist, "col": col}


@router.get("/collision-risk/{filename}")
def collision_risk(filename: str):
    df = load_file(filename)

    col = _get_best_column(df, ["collision_risk", "risk", "vru_label"])
    if not col:
        raise HTTPException(status_code=400, detail="Column 'collision_risk' not found")

    dist = _series_counts_to_dict(df[col].value_counts())
    return {"collision_risk_distribution": dist, "col": col}


@router.get("/environment/{filename}")
def environment_stats(filename: str):
    df = load_file(filename)

    out = {}
    wcol = _get_best_column(df, ["weather"])
    lcol = _get_best_column(df, ["light_condition", "lighting", "light"])

    if wcol:
        out["weather"] = _series_counts_to_dict(df[wcol].value_counts())
    if lcol:
        out["light_condition"] = _series_counts_to_dict(df[lcol].value_counts())
    if not out:
        raise HTTPException(status_code=400, detail="No 'weather' or 'light_condition' columns found")
    return out


@router.get("/vru-distance/{filename}")
def vru_distance_stats(filename: str):
    df = load_file(filename)

    col = _get_best_column(df, ["distance_to_vru_m", "vru_distance", "distance"])
    if not col:
        raise HTTPException(status_code=400, detail="Column 'distance_to_vru_m' not found")

    df[col] = pd.to_numeric(df[col], errors="coerce")
    df_clean = df[col].dropna()
    if df_clean.empty:
        raise HTTPException(status_code=400, detail=f"No numeric values found in '{col}'")

    data = {
        "col": col,
        "average_distance": _to_native(df_clean.mean()),
        "min_distance": _to_native(df_clean.min()),
        "max_distance": _to_native(df_clean.max()),
        "count": int(df_clean.count()),
        "distribution": _describe_to_native(df_clean.describe()),
    }

    return data


