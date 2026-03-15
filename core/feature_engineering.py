"""
feature_engineering.py
======================
Creates derived features from the cleaned surveillance DataFrame.

Derived columns
---------------
- ``age_group``       – categorical age bucket
- ``year``            – year extracted from ``datesick``
- ``month``           – month extracted from ``datesick``
- ``week``            – ISO week extracted from ``datesick``
- ``year_month``      – formatted ``YYYY-MM`` string for time-series charts
- ``reporting_delay`` – alias for ``days_to_report`` (kept for clarity)

FUTURE AI EXTENSION:
---------------------
New engineered features for ML models (e.g. rolling averages, lag features,
weather joins) should be added here so every consumer — dashboard *and*
ML pipeline — benefits from them.
"""

import pandas as pd

# ---------------------------------------------------------------------------
# Age-group bins
# ---------------------------------------------------------------------------
AGE_BINS = [0, 5, 15, 25, 35, 45, 55, 65, 200]
AGE_LABELS = ["0-4", "5-14", "15-24", "25-34", "35-44", "45-54", "55-64", "65+"]


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Return *df* with additional derived columns (in-place).

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned DataFrame from ``data_loader.load_and_clean()``.

    Returns
    -------
    pd.DataFrame
        Same DataFrame with new feature columns attached.
    """
    # --- Age group --------------------------------------------------------
    df["age_group"] = pd.cut(
        df["agey"], bins=AGE_BINS, labels=AGE_LABELS, right=False,
    )

    # --- Time dimensions from datesick ------------------------------------
    if "datesick" in df.columns:
        df["year"] = df["datesick"].dt.year.astype("Int64")
        df["month"] = df["datesick"].dt.month.astype("Int64")
        df["week"] = df["datesick"].dt.isocalendar().week.astype("Int64")
        df["year_month"] = df["datesick"].dt.to_period("M").astype(str)

    # --- Reporting delay (explicit alias) ---------------------------------
    if "days_to_report" in df.columns:
        df["reporting_delay"] = df["days_to_report"]

    # --- Diagnosis delay --------------------------------------------------
    if "days_to_define" in df.columns:
        df["diagnosis_delay"] = df["days_to_define"]

    return df
