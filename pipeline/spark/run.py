"""PySpark entry point: extract -> validate -> transform -> load (silver) -> Spark SQL (gold).

Usage:
    python -m pipeline.spark.run --source creditcard.csv --target output_spark/
"""
import argparse
import json
import sys
from pathlib import Path
from .session import get_spark
from . import quality, transform, aggregates


def main(source: str, target: str, master: str | None = "local[*]") -> int:
    spark = get_spark(master=master)
    raw = spark.read.csv(source, header=True, inferSchema=True)
    rows_in = raw.count()
    print(f"[extract] read {rows_in:,} rows from {source}")

    results = quality.run_all(raw)
    status = "passed" if all(r["passed"] for r in results) else "failed"
    for r in results:
        print(f"[quality] {r['check']:<10} {'PASS' if r['passed'] else 'FAIL'}")

    rows_out = 0
    if results[0]["passed"]:
        curated = transform.add_features(transform.clean(raw)).cache()
        rows_out = curated.count()
        curated.write.mode("overwrite").partitionBy("day").parquet(f"{target}/silver/transactions")
        for name, df in aggregates.build_gold(spark, curated).items():
            df.coalesce(1).write.mode("overwrite").parquet(f"{target}/gold/{name}")
            print(f"[gold] wrote {name}")

    Path(target).mkdir(parents=True, exist_ok=True)
    report = {"engine": "pyspark", "rows_in": rows_in, "rows_out": rows_out, "checks": results, "status": status}
    (Path(target) / "quality_report.json").write_text(json.dumps(report, indent=2))
    print(f"[run] status: {status}")
    spark.stop()
    return 0 if status == "passed" else 2


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--source", required=True)
    p.add_argument("--target", default="output_spark")
    p.add_argument("--master", default="local[*]", help="Spark master; pass '' on Databricks")
    a = p.parse_args()
    sys.exit(main(a.source, a.target, a.master or None))
