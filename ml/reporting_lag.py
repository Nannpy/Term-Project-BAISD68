"""
reporting_lag.py
================
Reporting Lag Prediction Model.

This module provides:
  • Prediction of reporting lag (in days) using ``reportinglag.pkl``
  • A fallback simulation if the model is not found
"""

import os
import hashlib
import numpy as np
import pandas as pd

_lag_model = None

def _try_load_pkl():
    """Attempt to load ``reportinglag.pkl`` from the project models dir."""
    global _lag_model
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    candidates = [
        os.path.join(project_root, "models", "reportinglag.pkl"),
        os.path.join(project_root, "reportinglag.pkl"),
        os.path.join(project_root, "ml", "reportinglag.pkl"),
    ]
    for path in candidates:
        if os.path.isfile(path):
            try:
                import joblib
                _lag_model = joblib.load(path)
                return True
            except Exception:
                try:
                    import pickle
                    with open(path, "rb") as f:
                        _lag_model = pickle.load(f)
                    return True
                except Exception:
                    pass
    return False

_model_available = _try_load_pkl()

def _simulate_lag(df: pd.DataFrame, province: str, district: str) -> float:
    """Generate a deterministic simulated reporting lag in days."""
    subset = df.copy()
    if province and "province" in subset.columns:
        subset = subset[subset["province"] == province]
    if district and "district" in subset.columns:
        subset = subset[subset["district"] == district]

    n_cases = len(subset)
    avg_delay = subset["days_to_report"].mean() if "days_to_report" in subset.columns and n_cases > 0 else 7.0

    seed_str = f"lag:{province or ''}:{district or ''}:{n_cases}"
    seed = int(hashlib.md5(seed_str.encode()).hexdigest()[:8], 16) % (10**6)
    rng = np.random.RandomState(seed)

    # Base is historical average + some random variation based on the deterministic seed
    base = avg_delay + rng.uniform(-2.0, 4.0)
    return max(0.0, round(base, 1))

def predict_lag(
    df: pd.DataFrame,
    province: str | None = None,
    district: str | None = None,
) -> dict:
    """Run reporting lag prediction for a given location."""
    global _lag_model, _model_available

    if _model_available and _lag_model is not None:
        try:
            from ml.feature_pipeline import prepare_features
            subset = df.copy()
            if province and "province" in subset.columns:
                subset = subset[subset["province"] == province]
            if district and "district" in subset.columns:
                subset = subset[subset["district"] == district]
            features = prepare_features(subset)
            lag = float(_lag_model.predict(features).mean())
            model_type = "trained"
        except Exception:
            lag = _simulate_lag(df, province, district)
            model_type = "simulated"
    else:
        lag = _simulate_lag(df, province, district)
        model_type = "simulated"

    return {
        "predicted_lag_days": lag,
        "model_type": model_type,
    }
