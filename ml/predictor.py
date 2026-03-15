"""
predictor.py
============
Central module for loading trained models and generating predictions.

The dashboard should call ``get_predictions(df)`` from this module
whenever ML predictions are needed — it should **never** contain
model logic directly.

FUTURE AI EXTENSION:
---------------------
How to integrate a new prediction model:

1. **Train your model** in ``ml/train_model.py`` (to be created).
   Save the trained artifact (pickle, joblib, ONNX, etc.) to a
   ``models/`` directory.

2. **Create a model class** that subclasses ``ml.model_interface.ModelInterface``
   and implements ``predict(input_df) -> prediction_df``.

3. **Register the model** in ``ml/model_registry.py`` (to be created)
   so the predictor can look it up by name::

       # ml/model_registry.py
       REGISTRY = {
           "outbreak":  OutbreakPredictor,
           "hotspot":   HotspotDetector,
           "delay":     ReportingDelayPredictor,
       }

4. **Update ``load_model()``** below to load the correct model class
   and its saved weights.

5. **Call from the dashboard** in ``ui/callbacks.py``::

       from ml.predictor import get_predictions
       preds = get_predictions(filtered_df, model_name="outbreak")
       fig = charts.prediction_chart(preds)

   The dashboard remains model-agnostic — it only calls this module.

Supported future models:
  • Outbreak prediction      — predict probability of outbreak next N days
  • Hotspot detection         — rank regions by risk score
  • Reporting delay prediction — estimate expected delay for new cases
"""

import pandas as pd
from ml.feature_pipeline import prepare_features

# ---------------------------------------------------------------------------
# Model cache (populated by load_model)
# ---------------------------------------------------------------------------
_model_cache: dict = {}


def load_model(model_name: str = "default"):
    """Load a trained model by name and cache it.

    Parameters
    ----------
    model_name : str
        Key in the model registry.

    Returns
    -------
    ModelInterface instance, or None if no model is available yet.
    """
    # TODO: Implement once models are trained and registered.
    #
    # Example:
    #   from ml.model_registry import REGISTRY
    #   model_cls = REGISTRY[model_name]
    #   model = model_cls()
    #   model.load_weights(f"models/{model_name}.pkl")
    #   _model_cache[model_name] = model
    #   return model
    return None


def get_predictions(
    df: pd.DataFrame,
    model_name: str = "default",
) -> pd.DataFrame | None:
    """Generate predictions for the given DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Raw or filtered surveillance DataFrame.
    model_name : str
        Which registered model to use.

    Returns
    -------
    pd.DataFrame or None
        Prediction results, or ``None`` if no model is loaded.
    """
    model = _model_cache.get(model_name) or load_model(model_name)
    if model is None:
        # No model available yet — return None so the dashboard
        # can gracefully skip the prediction section.
        return None

    features = prepare_features(df)
    return model.predict(features)
