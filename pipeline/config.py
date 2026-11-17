"""Pipeline configuration: expected schema and data quality thresholds."""

FEATURE_COLUMNS = [f"V{i}" for i in range(1, 29)]
EXPECTED_COLUMNS = ["Time", *FEATURE_COLUMNS, "Amount", "Class"]

# Data quality rules
AMOUNT_MIN = 0.0
VALID_CLASSES = {0, 1}
MAX_NULL_RATIO = 0.0          # no nulls allowed in curated output
MAX_DUPLICATE_RATIO = 0.01    # fail the run if >1% of rows are duplicates
