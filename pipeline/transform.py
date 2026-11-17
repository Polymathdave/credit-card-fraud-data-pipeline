"""Transform: clean raw records and add derived columns for analytics."""
import pandas as pd
from . import config


def clean(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    out = (
        df[config.EXPECTED_COLUMNS]
        .dropna()
        .drop_duplicates()
        .loc[lambda d: (d["Amount"] >= config.AMOUNT_MIN) & d["Class"].isin(config.VALID_CLASSES)]
        .copy()
    )
    out["Class"] = out["Class"].astype("int8")
    print(f"[transform] cleaned {before:,} -> {len(out):,} rows")
    return out


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["hour_of_day"] = ((out["Time"] // 3600) % 24).astype("int8")
    out["day"] = (out["Time"] // 86400).astype("int8")   # 0 or 1 in the 48-hour window
    out["amount_bucket"] = pd.cut(
        out["Amount"], bins=[-0.01, 10, 50, 200, 1000, float("inf")],
        labels=["0-10", "10-50", "50-200", "200-1000", "1000+"],
    ).astype(str)
    return out
