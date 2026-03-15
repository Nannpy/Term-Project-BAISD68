"""
outbreak_warning.py
===================
Outbreak Early Warning System for the Disease Surveillance Dashboard.

This module provides:
  • Risk-level evaluation based on hotspot probability
  • Hotspot probability prediction (tries .pkl model, falls back to simulation)
  • In-memory alert logging for tracking historical outbreak warnings

Risk Levels
-----------
  0.0 – 0.4  →  LOW
  0.4 – 0.7  →  MEDIUM
  0.7 – 0.8  →  HIGH
  0.8 – 1.0  →  OUTBREAK ALERT
"""

import os
import hashlib
from datetime import datetime

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Risk-level thresholds
# ---------------------------------------------------------------------------
RISK_LEVELS = [
    (0.8, "OUTBREAK ALERT"),
    (0.7, "HIGH"),
    (0.4, "MEDIUM"),
    (0.0, "LOW"),
]


def evaluate_risk(probability: float) -> str:
    """Map a hotspot probability to a human-readable risk level.

    Parameters
    ----------
    probability : float
        Value between 0.0 and 1.0.

    Returns
    -------
    str
        One of: ``"LOW"``, ``"MEDIUM"``, ``"HIGH"``, ``"OUTBREAK ALERT"``.
    """
    for threshold, label in RISK_LEVELS:
        if probability >= threshold:
            return label
    return "LOW"


# ---------------------------------------------------------------------------
# Model loading (with fallback to simulation)
# ---------------------------------------------------------------------------
_hotspot_model = None


def _try_load_pkl():
    """Attempt to load ``diseasehotspot.pkl`` from the project models dir."""
    global _hotspot_model
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    candidates = [
        os.path.join(project_root, "models", "diseasehotspot.pkl"),
        os.path.join(project_root, "diseasehotspot.pkl"),
        os.path.join(project_root, "ml", "diseasehotspot.pkl"),
    ]
    for path in candidates:
        if os.path.isfile(path):
            try:
                import joblib
                _hotspot_model = joblib.load(path)
                print(f" ✓ Loaded hotspot model from {path}")
                return True
            except Exception:
                try:
                    import pickle
                    with open(path, "rb") as f:
                        _hotspot_model = pickle.load(f)
                    print(f" ✓ Loaded hotspot model from {path}")
                    return True
                except Exception:
                    pass
    return False


# Try once at import time
_model_available = _try_load_pkl()


def _simulate_probability(df: pd.DataFrame, province: str, district: str) -> tuple[float, dict]:
    """Generate a deterministic simulated hotspot probability.

    Uses actual data features to produce a realistic-looking probability
    that is consistent for the same province/district combination.  This
    allows the full early-warning UI to function without a trained model.

    Returns
    -------
    tuple[float, dict]
        (probability, feature_scores) where feature_scores maps feature
        names to their contribution scores (0–1).
    """
    subset = df.copy()
    if province and "province" in subset.columns:
        subset = subset[subset["province"] == province]
    if district and "district" in subset.columns:
        subset = subset[subset["district"] == district]

    # Compute data-driven features
    n_cases = len(subset)
    death_rate = subset["death"].mean() if "death" in subset.columns and n_cases > 0 else 0
    avg_delay = subset["days_to_report"].mean() if "days_to_report" in subset.columns and n_cases > 0 else 0
    avg_age = subset["agey"].mean() if "agey" in subset.columns and n_cases > 0 else 0

    # Deterministic hash so the same inputs always produce the same output
    seed_str = f"{province or ''}:{district or ''}:{n_cases}"
    seed = int(hashlib.md5(seed_str.encode()).hexdigest()[:8], 16) % (10**6)
    rng = np.random.RandomState(seed)

    # Base probability from a blend of real features and randomness
    base = 0.3
    base += min(death_rate * 2.0, 0.3)           # death rate pushes risk up
    base += min(avg_delay / 100.0, 0.15)          # slow reporting → higher risk
    base += rng.uniform(-0.15, 0.25)              # variability
    probability = float(np.clip(base, 0.0, 0.99))

    feature_scores = {
        "Case Count": round(min(n_cases / 5000, 1.0), 3),
        "Death Rate": round(min(death_rate * 5, 1.0), 3),
        "Avg Reporting Delay": round(min(avg_delay / 30, 1.0), 3),
        "Avg Patient Age": round(min(avg_age / 80, 1.0), 3),
        "Population Density": round(rng.uniform(0.2, 0.8), 3),
        "Seasonal Factor": round(rng.uniform(0.1, 0.7), 3),
    }

    return probability, feature_scores


def predict_hotspot(
    df: pd.DataFrame,
    province: str | None = None,
    district: str | None = None,
) -> dict:
    """Run disease hotspot prediction for a given location.

    Parameters
    ----------
    df : pd.DataFrame
        The full cleaned surveillance DataFrame.
    province : str, optional
        Province to predict for.
    district : str, optional
        District to predict for.

    Returns
    -------
    dict
        Keys: ``probability``, ``risk_level``, ``feature_scores``,
        ``province``, ``district``, ``model_type``.
    """
    global _hotspot_model, _model_available

    if _model_available and _hotspot_model is not None:
        # --- Real model path (when .pkl exists) ---------------------------
        try:
            from ml.feature_pipeline import prepare_features
            subset = df.copy()
            if province and "province" in subset.columns:
                subset = subset[subset["province"] == province]
            if district and "district" in subset.columns:
                subset = subset[subset["district"] == district]
            features = prepare_features(subset)
            proba = _hotspot_model.predict_proba(features)[:, 1].mean()
            probability = float(np.clip(proba, 0.0, 0.99))
            feature_scores = {}
            if hasattr(_hotspot_model, "feature_importances_"):
                names = features.columns.tolist()
                imps = _hotspot_model.feature_importances_
                feature_scores = {
                    n: round(float(v), 3)
                    for n, v in zip(names, imps)
                }
            model_type = "trained"
        except Exception:
            probability, feature_scores = _simulate_probability(df, province, district)
            model_type = "simulated"
    else:
        # --- Simulated prediction path ------------------------------------
        probability, feature_scores = _simulate_probability(df, province, district)
        model_type = "simulated"

    risk_level = evaluate_risk(probability)

    return {
        "probability": round(probability, 4),
        "risk_level": risk_level,
        "feature_scores": feature_scores,
        "province": province or "All",
        "district": district or "All",
        "model_type": model_type,
    }


# ---------------------------------------------------------------------------
# Alert logging (in-memory)
# ---------------------------------------------------------------------------
_alert_log: list[dict] = []


def log_alert(province: str, district: str, probability: float) -> None:
    """Append an alert record to the in-memory alert log."""
    _alert_log.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "province": province or "All",
        "district": district or "All",
        "hotspot_probability": round(probability, 4),
        "risk_level": evaluate_risk(probability),
    })


def get_alert_log() -> list[dict]:
    """Return the full alert log (newest first)."""
    return list(reversed(_alert_log))
