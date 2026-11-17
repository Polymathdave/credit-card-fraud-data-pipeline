"""Entry point: extract -> validate -> transform -> load.

Usage:
    python -m pipeline.run --source creditcard.xlsx --target output/
"""
import argparse
import sys
from . import extract, quality, transform, load


def main(source: str, target: str) -> int:
    raw = extract.read_raw(source)

    results = quality.run_all(raw)
    if not results[0]["passed"]:
        print(f"[quality] schema check failed: {results[0]['missing_columns']}")
        load.write_report(results, len(raw), 0, target)
        return 1

    curated = transform.add_features(transform.clean(raw))
    load.write_parquet(curated, f"{target}/curated/transactions")
    report = load.write_report(results, len(raw), len(curated), target)

    for r in results:
        print(f"[quality] {r['check']:<10} {'PASS' if r['passed'] else 'FAIL'}")
    print(f"[run] status: {report['status']}")
    return 0 if report["status"] == "passed" else 2


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--source", required=True)
    p.add_argument("--target", default="output")
    a = p.parse_args()
    sys.exit(main(a.source, a.target))
