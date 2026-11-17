"""SparkSession factory. Uses local mode by default; on Databricks the existing session is reused."""
from pyspark.sql import SparkSession


def get_spark(app_name: str = "fraud-pipeline", master: str | None = None) -> SparkSession:
    builder = SparkSession.builder.appName(app_name).config("spark.sql.shuffle.partitions", "8")
    if master:
        builder = builder.master(master)
    return builder.getOrCreate()
