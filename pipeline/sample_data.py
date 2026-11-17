"""Generate a synthetic sample file with the same schema as the real dataset.

The real credit card dataset is not stored in this repo, so this lets anyone run
the pipeline end to end straight after cloning.

Usage:
    python -m pipeline.sample_data --rows 1000 --out data/sample_transactions.csv
"""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from . import config


def generate(rows: int = 1000, fraud_rate: float = 0.02, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    df = pd.DataFrame(rng.normal(size=(rows, 28)).round(4), columns=config.FEATURE_COLUMNS)
    df.insert(0, "Time", np.sort(rng.integers(0, 172_800, rows)).astype(float))
    df["Amount"] = rng.gamma(shape=1.5, scale=60, size=rows).round(2)
    df["Class"] = (rng.random(rows) < fraud_rate).astype(int)
    return df


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--rows", type=int, default=1000)
    p.add_argument("--out", default="data/sample_transactions.csv")
    a = p.parse_args()
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    generate(a.rows).to_csv(a.out, index=False)
    print(f"[sample] wrote {a.rows:,} synthetic rows to {a.out}")
