"""Data quality checks. Each check returns a result dict for the run report."""
import pandas as pd
from . import config


def check_schema(df: pd.DataFrame) -> dict:
    missing = [c for c in config.EXPECTED_COLUMNS if c not in df.columns]
    return {"check": "schema", "passed": not missing, "missing_columns": missing}


def check_nulls(df: pd.DataFrame) -> dict:
    ratio = float(df[config.EXPECTED_COLUMNS].isna().mean().max())
    return {"check": "nulls", "passed": ratio <= config.MAX_NULL_RATIO, "max_null_ratio": round(ratio, 6)}


def check_duplicates(df: pd.DataFrame) -> dict:
    ratio = float(df.duplicated().mean()) if len(df) else 0.0
    return {"check": "duplicates", "passed": ratio <= config.MAX_DUPLICATE_RATIO, "duplicate_ratio": round(ratio, 6)}


def check_domain(df: pd.DataFrame) -> dict:
    bad_amount = int((df["Amount"] < config.AMOUNT_MIN).sum())
    bad_class = int((~df["Class"].isin(config.VALID_CLASSES)).sum())
    return {"check": "domain", "passed": bad_amount == 0 and bad_class == 0,
            "negative_amounts": bad_amount, "invalid_class_labels": bad_class}


def run_all(df: pd.DataFrame) -> list[dict]:
    schema = check_schema(df)
    if not schema["passed"]:
        return [schema]
    return [schema, check_nulls(df), check_duplicates(df), check_domain(df)]
