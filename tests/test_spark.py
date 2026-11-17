"""PySpark tests, including a parity check against the pandas implementation."""
import numpy as np
import pandas as pd
import pytest

pyspark = pytest.importorskip("pyspark")

from pipeline import transform as pd_transform
from pipeline.spark import quality, transform, aggregates
from pipeline.spark.session import get_spark
from tests.test_pipeline import make_df


@pytest.fixture(scope="module")
def spark():
    s = get_spark("tests", master="local[2]")
    yield s
    s.stop()


def dirty_df():
    df = make_df(200)
    df.loc[0, "Amount"] = -5
    df.loc[1, "Class"] = 7
    df.loc[2, "V1"] = np.nan
    return pd.concat([df, df.iloc[[10]]], ignore_index=True)


def test_quality_flags_bad_data(spark):
    results = {r["check"]: r for r in quality.run_all(spark.createDataFrame(dirty_df()))}
    assert results["schema"]["passed"]
    assert not results["nulls"]["passed"]
    assert results["domain"]["negative_amounts"] == 1
    assert results["domain"]["invalid_class_labels"] == 1


def test_spark_matches_pandas(spark):
    pdf = dirty_df()
    expected = pd_transform.add_features(pd_transform.clean(pdf))
    actual = transform.add_features(transform.clean(spark.createDataFrame(pdf))).toPandas()
    assert len(actual) == len(expected) == 197
    cols = ["hour_of_day", "day", "amount_bucket"]
    key = ["Time", "Amount"]
    e = expected.sort_values(key)[key + cols].reset_index(drop=True)
    a = actual.sort_values(key)[key + cols].reset_index(drop=True)
    pd.testing.assert_frame_equal(a, e, check_dtype=False)


def test_gold_sql_tables(spark):
    curated = transform.add_features(transform.clean(spark.createDataFrame(make_df(500))))
    gold = aggregates.build_gold(spark, curated)
    assert set(gold) == {"fraud_by_hour", "fraud_by_amount_bucket"}
    by_hour = gold["fraud_by_hour"].toPandas()
    assert by_hour["transactions"].sum() == 500
    assert by_hour["hour_of_day"].between(0, 23).all()
