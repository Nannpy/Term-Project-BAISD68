"""
feature_pipeline.py
===================
Prepares model-input features from the cleaned surveillance DataFrame.

This module sits between ``core.feature_engineering`` (which creates
dashboard-level features) and the ML models that need numeric,
normalised feature matrices.

FUTURE AI EXTENSION:
---------------------
Steps to add new features for a model:

1. Add feature computation logic in ``prepare_features()``.
2. Update ``FEATURE_COLUMNS`` so the predictor knows which columns
   to select.
3. If the model needs external data (e.g. weather), add a join step
   here — keep the dashboard layer unaware of model-specific data.

Example features you might add:
 - Rolling 7-day / 14-day case averages
 - Lag features (cases last week, last month)
 - Weather variables (temperature, humidity, rainfall)
 - Population-normalised incidence rates
"""

import pandas as pd

# Columns that a trained model would typically expect
FEATURE_COLUMNS = [
    "agey",
    "death",
    "days_to_report",
    "days_to_define",
    # Add more as models require
]


def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    """Transform the surveillance DataFrame into a model-ready feature matrix.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned + engineered DataFrame (output of
        ``core.feature_engineering.add_features``).

    Returns
    -------
    pd.DataFrame
        Feature DataFrame suitable for ``ModelInterface.predict()``.
    """
    # Select relevant columns (placeholder — extend as needed)
    available = [c for c in FEATURE_COLUMNS if c in df.columns]
    features = df[available].copy()

    # Fill any remaining NaN with 0
    features = features.fillna(0)

    # Future: add scaling, encoding, rolling aggregates, etc.

    return features
