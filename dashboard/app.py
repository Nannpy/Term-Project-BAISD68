"""
app.py
======
Main entry point for the Disease Surveillance Analytics Dashboard.

Run with:
    python dashboard/app.py

The dashboard will be available at http://127.0.0.1:8050

ARCHITECTURE NOTES:
-------------------
This file only orchestrates the application.  All logic lives in the
modular packages:

  core/           – data loading, feature engineering, KPI computation
  visualization/  – Plotly chart factories and theme tokens
  ui/             – layout, callbacks, filters
  ml/             – (future) ML model integration

This separation allows the same core + visualization modules to be
reused in Flask, FastAPI, Streamlit, or React frontends without
modifying any business logic.

FUTURE AI EXTENSION:
---------------------
To surface ML predictions in the dashboard:

1. Train a model and save it (see ``ml/predictor.py`` for details).
2. In ``ui/callbacks.py``, call ``ml.predictor.get_predictions(df)``
   inside the ``update_dashboard`` callback.
3. Pass the predictions to new chart functions in
   ``visualization/charts.py`` (e.g. ``prediction_chart(preds)``).
4. Add a new tab or section in ``ui/layout.py`` to display the
   prediction charts.

No changes to this file are needed — the modular design keeps the
app entry point clean.
"""

import sys
import os

# ---------------------------------------------------------------------------
# Ensure the project root is on sys.path so that "core", "visualization",
# "ui", and "ml" are importable regardless of the working directory.
# ---------------------------------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ---------------------------------------------------------------------------
# Imports (after path setup)
# ---------------------------------------------------------------------------
from dash import Dash

from core.data_loader import load_and_clean
from core.feature_engineering import add_features
from visualization.theme import EXTERNAL_STYLESHEETS, PAGE_STYLE
from ui.layout import build_layout
from ui.callbacks import register_callbacks


def create_app() -> Dash:
    """Factory function that creates and returns a configured Dash app.

    This factory pattern makes it easy to embed the dashboard inside
    a Flask or FastAPI server later::

        from dashboard.app import create_app
        dash_app = create_app()
        flask_server = dash_app.server  # underlying Flask instance
    """
    # --- Load and prepare data --------------------------------------------
    print(" Loading dataset...")
    df = load_and_clean()
    print(f" Loaded {len(df):,} records.")

    print(" Engineering features...")
    df = add_features(df)

    # --- Create Dash app --------------------------------------------------
    app = Dash(
        __name__,
        external_stylesheets=EXTERNAL_STYLESHEETS,
        title="Disease Surveillance Analytics",
        update_title="Loading...",
        suppress_callback_exceptions=True,
    )

    # --- Set layout -------------------------------------------------------
    app.layout = build_layout(df)

    # --- Register callbacks -----------------------------------------------
    register_callbacks(app, df)

    return app


# ---------------------------------------------------------------------------
# Run the development server
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app = create_app()
    print(" Dashboard ready — open http://127.0.0.1:8050")
    app.run(debug=False, host="127.0.0.1", port=8050)
