"""
filters.py
==========
Dash filter components and a helper to apply filters to a DataFrame.

Each ``create_*_filter`` function returns a Dash ``html.Div`` containing
a label and a ``dcc.Dropdown``.  The ``apply_filters`` function takes the
raw DataFrame plus filter values and returns the filtered subset.
"""

from dash import dcc, html
import pandas as pd

from visualization.theme import FILTER_ITEM_STYLE, TEXT_PRIMARY, TEXT_SECONDARY

_LABEL_STYLE = {
    "fontSize": "12px",
    "fontWeight": "600",
    "color": TEXT_SECONDARY,
    "marginBottom": "4px",
    "textTransform": "uppercase",
    "letterSpacing": "0.4px",
}

_DROPDOWN_STYLE = {
    "fontSize": "13px",
}


def _sorted_unique(series: pd.Series):
    """Return sorted unique non-null values from a Series."""
    vals = series.dropna().unique().tolist()
    try:
        return sorted(vals)
    except TypeError:
        return sorted(vals, key=str)


# ---------------------------------------------------------------------------
# Filter component factories
# ---------------------------------------------------------------------------

def create_year_filter(df: pd.DataFrame) -> html.Div:
    options = _sorted_unique(df["year"]) if "year" in df.columns else []
    return html.Div([
        html.Label("Year", style=_LABEL_STYLE),
        dcc.Dropdown(
            id="filter-year",
            options=[{"label": str(int(y)), "value": int(y)} for y in options],
            value=None,
            placeholder="All Years",
            clearable=True,
            style=_DROPDOWN_STYLE,
        ),
    ], style=FILTER_ITEM_STYLE)


def create_province_filter(df: pd.DataFrame) -> html.Div:
    options = _sorted_unique(df["province"]) if "province" in df.columns else []
    return html.Div([
        html.Label("Province", style=_LABEL_STYLE),
        dcc.Dropdown(
            id="filter-province",
            options=[{"label": p, "value": p} for p in options],
            value=None,
            placeholder="All Provinces",
            clearable=True,
            style=_DROPDOWN_STYLE,
        ),
    ], style=FILTER_ITEM_STYLE)


def create_district_filter(df: pd.DataFrame) -> html.Div:
    options = _sorted_unique(df["district"]) if "district" in df.columns else []
    return html.Div([
        html.Label("District", style=_LABEL_STYLE),
        dcc.Dropdown(
            id="filter-district",
            options=[{"label": d, "value": d} for d in options],
            value=None,
            placeholder="All Districts",
            clearable=True,
            style=_DROPDOWN_STYLE,
        ),
    ], style=FILTER_ITEM_STYLE)


def create_sex_filter(df: pd.DataFrame) -> html.Div:
    options = _sorted_unique(df["Sex_en"]) if "Sex_en" in df.columns else []
    return html.Div([
        html.Label("Sex", style=_LABEL_STYLE),
        dcc.Dropdown(
            id="filter-sex",
            options=[{"label": s, "value": s} for s in options],
            value=None,
            placeholder="All",
            clearable=True,
            style=_DROPDOWN_STYLE,
        ),
    ], style=FILTER_ITEM_STYLE)


def create_age_group_filter(df: pd.DataFrame) -> html.Div:
    options = _sorted_unique(df["age_group"]) if "age_group" in df.columns else []
    return html.Div([
        html.Label("Age Group", style=_LABEL_STYLE),
        dcc.Dropdown(
            id="filter-age-group",
            options=[{"label": str(a), "value": str(a)} for a in options],
            value=None,
            placeholder="All",
            clearable=True,
            style=_DROPDOWN_STYLE,
        ),
    ], style=FILTER_ITEM_STYLE)


# ---------------------------------------------------------------------------
# Apply filters
# ---------------------------------------------------------------------------

def apply_filters(
    df: pd.DataFrame,
    year=None,
    province=None,
    district=None,
    sex=None,
    age_group=None,
) -> pd.DataFrame:
    """Return a filtered copy of *df* based on the provided filter values.

    Any filter set to ``None`` is ignored (i.e. 'show all').
    """
    filtered = df.copy()

    if year is not None:
        filtered = filtered[filtered["year"] == year]
    if province is not None:
        filtered = filtered[filtered["province"] == province]
    if district is not None:
        filtered = filtered[filtered["district"] == district]
    if sex is not None:
        filtered = filtered[filtered["Sex_en"] == sex]
    if age_group is not None:
        filtered = filtered[filtered["age_group"].astype(str) == str(age_group)]

    return filtered
