"""Data quality checks implemented with PySpark (same rules as the pandas version)."""
from pyspark.sql import DataFrame, functions as F
from .. import config


def check_schema(df: DataFrame) -> dict:
    missing = [c for c in config.EXPECTED_COLUMNS if c not in df.columns]
    return {"check": "schema", "passed": not missing, "missing_columns": missing}


def check_nulls(df: DataFrame) -> dict:
    total = df.count()
    null_counts = df.select(
        [F.sum((F.col(c).isNull() | F.isnan(c)).cast("int")).alias(c) for c in config.EXPECTED_COLUMNS]
    ).first().asDict()
    ratio = max(null_counts.values()) / total if total else 0.0
    return {"check": "nulls", "passed": ratio <= config.MAX_NULL_RATIO, "max_null_ratio": round(ratio, 6)}


def check_duplicates(df: DataFrame) -> dict:
    total = df.count()
    ratio = (total - df.dropDuplicates().count()) / total if total else 0.0
    return {"check": "duplicates", "passed": ratio <= config.MAX_DUPLICATE_RATIO, "duplicate_ratio": round(ratio, 6)}


def check_domain(df: DataFrame) -> dict:
    row = df.select(
        F.sum((F.col("Amount") < config.AMOUNT_MIN).cast("int")).alias("neg"),
        F.sum((~F.col("Class").isin(list(config.VALID_CLASSES))).cast("int")).alias("bad"),
    ).first()
    neg, bad = int(row["neg"] or 0), int(row["bad"] or 0)
    return {"check": "domain", "passed": neg == 0 and bad == 0,
            "negative_amounts": neg, "invalid_class_labels": bad}


def run_all(df: DataFrame) -> list[dict]:
    schema = check_schema(df)
    if not schema["passed"]:
        return [schema]
    return [schema, check_nulls(df), check_duplicates(df), check_domain(df)]
