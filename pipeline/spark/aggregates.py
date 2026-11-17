"""Gold layer: run the Spark SQL files in /sql against the curated transactions view."""
from pathlib import Path
from pyspark.sql import DataFrame, SparkSession

SQL_DIR = Path(__file__).resolve().parents[2] / "sql"


def build_gold(spark: SparkSession, curated: DataFrame) -> dict[str, DataFrame]:
    curated.createOrReplaceTempView("transactions")
    return {path.stem: spark.sql(path.read_text()) for path in sorted(SQL_DIR.glob("*.sql"))}
