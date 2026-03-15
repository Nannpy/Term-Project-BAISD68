"""
data_loader.py
==============
Responsible for loading datasets, parsing datetime columns, and basic cleaning.

This module is the single entry point for all raw data. Other modules
(feature_engineering, kpi_engine, charts) receive a clean DataFrame from here.

FUTURE AI EXTENSION:
---------------------
When adding ML models, the cleaned DataFrame returned by `load_and_clean()`
should be passed to `ml.feature_pipeline.prepare_features()` before feeding
it to `ml.predictor.get_predictions()`.
"""

import os
import pandas as pd

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
DATE_COLUMNS = ["datesick", "datedefine", "datefound", "datedeath"]

CATEGORICAL_COLUMNS = [
    "Sex", "nation", "occupat", "metropol", "treatmentloc",
    "patienttype", "results", "district", "province",
]

# Thai → English sex mapping for chart readability
SEX_MAP = {
    "ชาย": "Male",
    "หญิง": "Female",
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def load_and_clean(filepath: str | None = None) -> pd.DataFrame:
    """Load the surveillance CSV dataset and return a cleaned DataFrame.

    Parameters
    ----------
    filepath : str, optional
        Absolute path to the CSV file.  When *None*, the loader looks for
        ``df_all_clean (1).csv`` next to the project root.

    Returns
    -------
    pd.DataFrame
        Cleaned DataFrame ready for feature engineering and analysis.
    """
    if filepath is None:
        # Default: look relative to this file's grandparent (project root)
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filepath = os.path.join(project_root, "df_all_clean (1).csv")

    df = pd.read_csv(filepath, encoding="utf-8")

    # --- Parse datetime columns -------------------------------------------
    for col in DATE_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # --- Remove exact duplicate rows --------------------------------------
    df = df.drop_duplicates().reset_index(drop=True)

    # --- Handle missing values --------------------------------------------
    # Numeric columns: fill NaN with 0
    numeric_cols = df.select_dtypes(include="number").columns
    df[numeric_cols] = df[numeric_cols].fillna(0)

    # Categorical columns: fill NaN with "Unknown"
    for col in CATEGORICAL_COLUMNS:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown").astype(str).str.strip()

    # --- Standardise Sex to English labels --------------------------------
    df["Sex_en"] = df["Sex"].map(SEX_MAP).fillna("Unknown")

    # --- Ensure death column is integer -----------------------------------
    if "death" in df.columns:
        df["death"] = df["death"].astype(int)

    return df
