import numpy as np
import pandas as pd
from pipeline import config, quality, transform


def make_df(n=100, seed=0):
    rng = np.random.default_rng(seed)
    df = pd.DataFrame(rng.normal(size=(n, 28)), columns=config.FEATURE_COLUMNS)
    df.insert(0, "Time", rng.integers(0, 172_800, n).astype(float))
    df["Amount"] = rng.uniform(0, 500, n).round(2)
    df["Class"] = (rng.random(n) < 0.02).astype(int)
    return df


def test_clean_data_passes_all_checks():
    assert all(r["passed"] for r in quality.run_all(make_df()))


def test_missing_column_fails_schema():
    result = quality.run_all(make_df().drop(columns=["Amount"]))
    assert result[0]["check"] == "schema" and not result[0]["passed"]
    assert result[0]["missing_columns"] == ["Amount"]


def test_clean_removes_bad_rows():
    df = make_df()
    df.loc[0, "Amount"] = -5
    df.loc[1, "Class"] = 7
    df.loc[2, "V1"] = np.nan
    df = pd.concat([df, df.iloc[[10]]])
    out = transform.clean(df)
    assert len(out) == 97


def test_features_added():
    out = transform.add_features(transform.clean(make_df()))
    assert {"hour_of_day", "day", "amount_bucket"} <= set(out.columns)
    assert out["hour_of_day"].between(0, 23).all()
    assert set(out["day"].unique()) <= {0, 1}
