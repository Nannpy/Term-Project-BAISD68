# Disease Surveillance Analytics Dashboard

A modular, ML-ready analytics dashboard for infectious disease surveillance data, built with **Python**, **Pandas**, **Plotly**, and **Plotly Dash**.

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the dashboard
python dashboard/app.py

# 3. Open in browser
#    http://127.0.0.1:8050
```

---

## Project Structure

```
project/
├── dashboard/
│   └── app.py                  # Dash application entry point
├── core/
│   ├── data_loader.py          # Dataset loading & cleaning
│   ├── feature_engineering.py  # Derived features (age_group, week, etc.)
│   └── kpi_engine.py           # KPI computation (cases, deaths, CFR, etc.)
├── visualization/
│   ├── theme.py                # Design tokens, Plotly template, CSS styles
│   └── charts.py               # Reusable Plotly chart functions
├── ui/
│   ├── layout.py               # Dashboard layout (KPI cards, tabs, grid)
│   ├── callbacks.py            # Dash callbacks (filters → charts)
│   └── filters.py              # Filter components & apply logic
├── ml/
│   ├── model_interface.py      # Abstract base class for all models
│   ├── feature_pipeline.py     # Feature preparation for ML models
│   └── predictor.py            # Model loading & prediction API
├── requirements.txt
└── README.md
```

---

## Dashboard Sections

| Tab | Contents |
|---|---|
| **Overview** | KPI cards · Cases over time · Deaths over time · Weekly trends |
| **Geographic** | Cases by province · Cases by district |
| **Demographic** | Age distribution · Age groups · Sex distribution · Occupation |
| **Surveillance** | Reporting delay · Diagnosis delay · Avg delay by province |

All charts support interactive filters: **Year**, **Province**, **District**, **Sex**, **Age Group**.

---

## Integrating with Other Frameworks

The `create_app()` factory in `dashboard/app.py` returns a standard Dash app whose underlying Flask server is accessible via `app.server`:

```python
# Flask integration
from dashboard.app import create_app
dash_app = create_app()
flask_server = dash_app.server

# FastAPI integration (via WSGIMiddleware)
from fastapi import FastAPI
from starlette.middleware.wsgi import WSGIMiddleware
api = FastAPI()
api.mount("/dashboard", WSGIMiddleware(dash_app.server))
```

The `core/` and `visualization/` modules are framework-agnostic — import them directly in Streamlit or React backends.

---

## Adding ML Prediction Models

The `ml/` folder is pre-structured for plug-in prediction models. Follow these steps:

### Step 1 — Train a model

Create `ml/train_model.py`:

```python
# ml/train_model.py
from core.data_loader import load_and_clean
from core.feature_engineering import add_features
from ml.feature_pipeline import prepare_features

df = load_and_clean()
df = add_features(df)
features = prepare_features(df)

# Train your model (scikit-learn, XGBoost, PyTorch, etc.)
# Save to models/outbreak_model.pkl
```

### Step 2 — Implement the model interface

```python
# ml/outbreak_predictor.py
from ml.model_interface import ModelInterface
import joblib, pandas as pd

class OutbreakPredictor(ModelInterface):
    def __init__(self):
        self.model = joblib.load("models/outbreak_model.pkl")

    def predict(self, input_df: pd.DataFrame) -> pd.DataFrame:
        preds = self.model.predict(input_df)
        return pd.DataFrame({"prediction": preds})
```

### Step 3 — Register and load

Create `ml/model_registry.py`:

```python
REGISTRY = {
    "outbreak":  "ml.outbreak_predictor.OutbreakPredictor",
    "hotspot":   "ml.hotspot_detector.HotspotDetector",
    "delay":     "ml.delay_predictor.ReportingDelayPredictor",
}
```

Update `ml/predictor.py` → `load_model()` to read from the registry.

### Step 4 — Call from the dashboard

In `ui/callbacks.py`:

```python
from ml.predictor import get_predictions

preds = get_predictions(filtered_df, model_name="outbreak")
if preds is not None:
    fig = charts.prediction_chart(preds)  # add to visualization/charts.py
```

### Example Models

| Model | Input | Output |
|---|---|---|
| Outbreak Prediction | Weekly case counts, weather | Probability of outbreak |
| Hotspot Detection | Province-level time series | Risk score per region |
| Reporting Delay | Case metadata | Predicted delay (days) |

---

## License

Internal use — adapt as needed.
