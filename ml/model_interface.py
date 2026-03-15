"""
model_interface.py
==================
Defines the standard interface that **all** prediction models must follow.

Any model integrated into this system should subclass ``ModelInterface``
and implement the ``predict`` method.

FUTURE AI EXTENSION:
---------------------
Example models that can be created by subclassing this interface:

1. **OutbreakPredictor**  (``ml/train_model.py``)
   - Input:  weekly case counts, weather data, lag features
   - Output: probability of outbreak in next 2 weeks

2. **HotspotDetector**  (``ml/train_model.py``)
   - Input:  province/district-level case time series
   - Output: risk score per region

3. **ReportingDelayPredictor**  (``ml/train_model.py``)
   - Input:  case metadata (location, patient type, etc.)
   - Output: predicted reporting delay in days

All models should be registered in ``ml/model_registry.py`` (to be created)
and loaded via ``ml/predictor.py``.
"""

from abc import ABC, abstractmethod
import pandas as pd


class ModelInterface(ABC):
    """Standard interface for all prediction models.

    Every model must implement ``predict(input_df)`` which takes a
    DataFrame of input features and returns a DataFrame of predictions.
    """

    @abstractmethod
    def predict(self, input_df: pd.DataFrame) -> pd.DataFrame:
        """Generate predictions from the input DataFrame.

        Parameters
        ----------
        input_df : pd.DataFrame
            Feature DataFrame prepared by ``ml.feature_pipeline.prepare_features()``.

        Returns
        -------
        pd.DataFrame
            Predictions — structure depends on the specific model.
            At minimum, should contain a ``prediction`` column.
        """
        ...

    def get_model_name(self) -> str:
        """Human-readable model name for dashboard display."""
        return self.__class__.__name__
