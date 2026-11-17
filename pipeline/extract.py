"""Extract: read raw transaction files (CSV or Excel) into a DataFrame."""
from pathlib import Path
import pandas as pd


def read_raw(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if path.suffix.lower() in {".xlsx", ".xls"}:
        df = pd.read_excel(path)
    elif path.suffix.lower() == ".csv":
        df = pd.read_csv(path)
    else:
        raise ValueError(f"Unsupported file type: {path.suffix}")
    print(f"[extract] read {len(df):,} rows from {path.name}")
    return df
