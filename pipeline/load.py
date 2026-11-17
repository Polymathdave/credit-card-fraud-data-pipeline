"""Load: write curated data as partitioned Parquet plus a run report."""
import json
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd


def write_parquet(df: pd.DataFrame, target: str | Path) -> None:
    target = Path(target)
    target.mkdir(parents=True, exist_ok=True)
    df.to_parquet(target, partition_cols=["day"], index=False)
    print(f"[load] wrote {len(df):,} rows to {target} (partitioned by day)")


def write_report(results: list[dict], rows_in: int, rows_out: int, target: str | Path) -> dict:
    report = {
        "run_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "rows_in": rows_in,
        "rows_out": rows_out,
        "checks": results,
        "status": "passed" if all(r["passed"] for r in results) else "failed",
    }
    Path(target).mkdir(parents=True, exist_ok=True)
    (Path(target) / "quality_report.json").write_text(json.dumps(report, indent=2))
    return report
