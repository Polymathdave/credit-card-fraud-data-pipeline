# Credit Card Fraud: Data Pipeline & Analysis

[![tests](https://github.com/Polymathdave/credit-card-fraud-data-pipeline/actions/workflows/tests.yml/badge.svg)](https://github.com/Polymathdave/credit-card-fraud-data-pipeline/actions/workflows/tests.yml)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PySpark](https://img.shields.io/badge/PySpark-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white)
![Spark SQL](https://img.shields.io/badge/Spark%20SQL-1F6FEB?style=for-the-badge&logo=apachespark&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Parquet](https://img.shields.io/badge/Apache%20Parquet-50ABF1?style=for-the-badge)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)

A batch **ETL pipeline** that turns raw credit card transaction exports into a validated, analytics-ready **Parquet** dataset with an automated **data quality report**. It has two engines: **pandas** for small files and **PySpark** for larger volumes, with **Spark SQL** building the gold reporting tables. It is paired with an exploratory analysis of the data that informed the pipeline's validation rules and derived features.

## 🏗️ Architecture
```
 Raw export (.xlsx / .csv)
          │
          ▼
 ┌──────────────┐   read CSV or Excel
 │   EXTRACT    │
 └──────┬───────┘
        ▼
 ┌──────────────┐   schema · nulls · duplicates · domain rules
 │   VALIDATE   │──► quality_report.json (pass / fail per check)
 └──────┬───────┘
        ▼
 ┌──────────────┐   drop invalid rows, dedupe, type casting,
 │  TRANSFORM   │   derive hour_of_day, day, amount_bucket
 └──────┬───────┘
        ▼
 ┌──────────────┐
 │     LOAD     │──► curated/transactions/day=0|1/*.parquet
 └──────────────┘
```

## ⚡ PySpark engine
The same pipeline is implemented in PySpark (`pipeline/spark/`) using a medallion layout:

| Layer | What it holds | How it's built |
|-------|---------------|----------------|
| **Silver** | Validated, cleaned transactions with derived features, partitioned by `day` | PySpark DataFrame API |
| **Gold** | `fraud_by_hour`, `fraud_by_amount_bucket` reporting tables | Spark SQL queries in `sql/` |

A **parity test** runs the pandas and PySpark versions on the same input and checks that they produce identical results. The session factory runs in local mode by default and is written to reuse the existing session on Databricks (`--master ''`).

## ✅ Data quality checks
| Check | Rule | On failure |
|-------|------|------------|
| Schema | All 31 expected columns present (`Time`, `V1`–`V28`, `Amount`, `Class`) | Run stops, report written |
| Nulls | No nulls in curated columns | Flagged in report |
| Duplicates | ≤ 1% duplicate rows | Flagged in report |
| Domain | `Amount ≥ 0`, `Class ∈ {0, 1}` | Flagged in report |

The run exits with a non-zero code when any check fails, so a scheduler or CI job can alert on it.

## 📁 Project structure
```
├── pipeline/
│   ├── config.py      # Expected schema and quality thresholds
│   ├── extract.py     # Read raw CSV / Excel
│   ├── quality.py     # Data quality checks
│   ├── transform.py   # Cleaning and feature derivation
│   ├── load.py        # Partitioned Parquet + JSON run report
│   ├── run.py         # Pipeline entry point (pandas)
│   └── spark/         # PySpark engine: session, quality, transform, aggregates, run
├── sql/               # Spark SQL for gold tables
├── tests/             # Pytest unit tests incl. Spark/pandas parity (run in CI)
├── .github/workflows/ # GitHub Actions: tests on every push
├── implementation.ipynb  # Exploratory data analysis
└── requirements.txt
```

## ▶️ Run it
```bash
pip install -r requirements.txt

# pandas engine
python -m pipeline.run --source creditcard.xlsx --target output/

# PySpark engine (requires Java 17)
python -m pipeline.spark.run --source creditcard.csv --target output_spark/

pytest -q tests
```
PySpark output:
```
output_spark/
├── silver/transactions/day=0|1/*.parquet
├── gold/fraud_by_hour/*.parquet
├── gold/fraud_by_amount_bucket/*.parquet
└── quality_report.json
```

## 🔍 Exploratory analysis
`implementation.ipynb` profiles the dataset before the pipeline was built. It covers class imbalance, fraud by hour across the 48-hour window, amount distributions with a Mann-Whitney U test, and the anonymised PCA features (V1–V28) most correlated with fraud. These findings set the pipeline's validation rules and its derived `hour_of_day` and `amount_bucket` columns.

## 🗺️ Next steps
- [x] Port the pipeline to PySpark with Spark SQL gold tables
- [ ] Load curated data into a warehouse table (e.g. Databricks / Azure SQL)
- [ ] Schedule with Airflow and alert on failed quality checks
