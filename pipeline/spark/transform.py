"""Cleaning and feature derivation with the PySpark DataFrame API."""
from pyspark.sql import DataFrame, functions as F
from .. import config


def clean(df: DataFrame) -> DataFrame:
    return (
        df.select(*config.EXPECTED_COLUMNS)
        .dropna()
        .dropDuplicates()
        .filter((F.col("Amount") >= config.AMOUNT_MIN) & F.col("Class").isin(list(config.VALID_CLASSES)))
        .withColumn("Class", F.col("Class").cast("tinyint"))
    )


def add_features(df: DataFrame) -> DataFrame:
    amount = F.col("Amount")
    return (
        df.withColumn("hour_of_day", ((F.floor(F.col("Time") / 3600)) % 24).cast("tinyint"))
        .withColumn("day", F.floor(F.col("Time") / 86400).cast("tinyint"))
        .withColumn(
            "amount_bucket",
            F.when(amount <= 10, "0-10")
            .when(amount <= 50, "10-50")
            .when(amount <= 200, "50-200")
            .when(amount <= 1000, "200-1000")
            .otherwise("1000+"),
        )
    )
