"""
kpi_engine.py
=============
Computes high-level KPI metrics from a (possibly filtered) DataFrame.

Every function accepts a DataFrame so the dashboard can pass in a
pre-filtered subset and get KPIs that reflect the active filters.

FUTURE AI EXTENSION:
---------------------
Once ML models are integrated, you can add KPI functions here such as
``predicted_cases_next_week()`` or ``outbreak_probability()`` that call
``ml.predictor.get_predictions()`` internally.
"""

import pandas as pd


def total_cases(df: pd.DataFrame) -> int:
    """Total number of case records."""
    return len(df)


def total_deaths(df: pd.DataFrame) -> int:
    """Total number of deaths (``death == 1``)."""
    if "death" in df.columns:
        return int(df["death"].sum())
    return 0


def case_fatality_rate(df: pd.DataFrame) -> float:
    """Case fatality rate as a percentage."""
    cases = total_cases(df)
    if cases == 0:
        return 0.0
    return round(total_deaths(df) / cases * 100, 2)


def average_age(df: pd.DataFrame) -> float:
    """Mean patient age in years."""
    if "agey" in df.columns and len(df) > 0:
        return round(df["agey"].mean(), 1)
    return 0.0


def male_female_ratio(df: pd.DataFrame) -> str:
    """Return a human-readable male-to-female ratio string (e.g. '1.2 : 1')."""
    if "Sex_en" not in df.columns or len(df) == 0:
        return "N/A"
    counts = df["Sex_en"].value_counts()
    males = counts.get("Male", 0)
    females = counts.get("Female", 0)
    if females == 0:
        return f"{males} : 0"
    ratio = round(males / females, 2)
    return f"{ratio} : 1"


def compute_all(df: pd.DataFrame) -> dict:
    """Return a dict of all KPIs for the given DataFrame."""
    return {
        "total_cases": total_cases(df),
        "total_deaths": total_deaths(df),
        "cfr": case_fatality_rate(df),
        "avg_age": average_age(df),
        "mf_ratio": male_female_ratio(df),
    }
