"""
layout.py
=========
Defines the full Dash layout: header, filter bar, KPI cards, and tabbed
chart sections (Overview, Geographic, Demographic, Surveillance, Prediction).

The layout uses a responsive CSS-grid approach via Dash ``html`` components
and inline styles defined in ``visualization.theme``.
"""

from dash import dcc, html, dash_table
import pandas as pd

from visualization.theme import (
    PAGE_STYLE, CARD_STYLE, KPI_CARD_STYLE, KPI_VALUE_STYLE,
    KPI_LABEL_STYLE, CHART_CARD_STYLE, FILTER_CONTAINER_STYLE,
    HEADER_STYLE, SUBHEADER_STYLE, TAB_STYLE, TAB_SELECTED_STYLE,
    PRIMARY, PRIMARY_LIGHT, DANGER, SUCCESS, ACCENT, TEXT_SECONDARY,
    PREDICTION_CARD_STYLE, PREDICTION_BUTTON_STYLE,
    FILTER_ITEM_STYLE, BG_CARD, TEXT_PRIMARY, BORDER, FONT_FAMILY,
)
from ui.filters import (
    create_year_filter,
    create_province_filter,
    create_district_filter,
    create_sex_filter,
    create_age_group_filter,
)


# ---------------------------------------------------------------------------
# KPI cards
# ---------------------------------------------------------------------------

def _kpi_card(card_id: str, label: str, icon: str, color: str = PRIMARY) -> html.Div:
    """Build a single KPI card with an icon, value placeholder, and label."""
    return html.Div([
        html.Div(icon, style={
            "fontSize": "28px", "marginBottom": "4px",
        }),
        html.Div(id=card_id, children="—", style={**KPI_VALUE_STYLE, "color": color}),
        html.Div(label, style=KPI_LABEL_STYLE),
    ], style=KPI_CARD_STYLE)


def _kpi_row() -> html.Div:
    """Row of five KPI cards."""
    return html.Div([
        _kpi_card("kpi-total-cases",  "Total Cases",       "📊", PRIMARY),
        _kpi_card("kpi-total-deaths", "Total Deaths",      "⚠️", DANGER),
        _kpi_card("kpi-cfr",          "Case Fatality Rate", "📈", DANGER),
        _kpi_card("kpi-avg-age",      "Average Age",       "👤", ACCENT),
        _kpi_card("kpi-mf-ratio",     "Male : Female",     "👥", SUCCESS),
    ], style={
        "display": "flex",
        "gap": "16px",
        "flexWrap": "wrap",
        "marginBottom": "20px",
    })


# ---------------------------------------------------------------------------
# Chart grid helpers
# ---------------------------------------------------------------------------

def _chart_row(*graph_ids, heights=None) -> html.Div:
    """Create a responsive row of ``dcc.Graph`` components."""
    children = []
    n = len(graph_ids)
    for i, gid in enumerate(graph_ids):
        h = (heights[i] if heights else 380)
        children.append(
            html.Div(
                dcc.Graph(id=gid, config={"displayModeBar": False}, style={"height": f"{h}px"}),
                style={**CHART_CARD_STYLE, "flex": "1", "minWidth": "400px"},
            )
        )
    return html.Div(children, style={"display": "flex", "gap": "16px", "flexWrap": "wrap"})


# ---------------------------------------------------------------------------
# Tab contents
# ---------------------------------------------------------------------------

def _tab_overview() -> html.Div:
    return html.Div([
        _chart_row("chart-cases-time", "chart-deaths-time"),
        _chart_row("chart-weekly-trends"),
    ])


def _tab_geographic() -> html.Div:
    return html.Div([
        _chart_row("chart-province", "chart-district", heights=[500, 500]),
    ])


def _tab_demographic() -> html.Div:
    return html.Div([
        _chart_row("chart-age-dist", "chart-sex-dist"),
        _chart_row("chart-age-group", "chart-occupation"),
    ])


def _tab_surveillance() -> html.Div:
    return html.Div([
        _chart_row("chart-report-delay", "chart-diag-delay"),
        _chart_row("chart-delay-province"),
    ])


def _tab_prediction(df: pd.DataFrame) -> html.Div:
    """Build the Prediction tab with province/district selectors, predict
    button, and placeholders for alert, result, gauge, feature chart, and
    alert history table."""

    # Unique provinces/districts for the dropdowns
    provinces = sorted(df["province"].dropna().unique().tolist()) if "province" in df.columns else []
    districts = sorted(df["district"].dropna().unique().tolist()) if "district" in df.columns else []

    _label_style = {
        "fontSize": "12px", "fontWeight": "600", "color": TEXT_SECONDARY,
        "marginBottom": "4px", "textTransform": "uppercase", "letterSpacing": "0.4px",
    }

    return html.Div([
        # --- Input controls -----------------------------------------------
        html.Div([
            html.Div([
                html.Label("Province", style=_label_style),
                dcc.Dropdown(
                    id="pred-province",
                    options=[{"label": p, "value": p} for p in provinces],
                    value=None, placeholder="Select Province",
                    clearable=True, style={"fontSize": "13px"},
                ),
            ], style={**FILTER_ITEM_STYLE, "minWidth": "200px"}),

            html.Div([
                html.Label("District", style=_label_style),
                dcc.Dropdown(
                    id="pred-district",
                    options=[{"label": d, "value": d} for d in districts],
                    value=None, placeholder="Select District",
                    clearable=True, style={"fontSize": "13px"},
                ),
            ], style={**FILTER_ITEM_STYLE, "minWidth": "200px"}),

            html.Div([
                html.Label(" ", style=_label_style),  # spacer
                html.Button(
                    "🔍 Run Prediction",
                    id="btn-predict",
                    n_clicks=0,
                    style=PREDICTION_BUTTON_STYLE,
                ),
            ], style={"display": "flex", "flexDirection": "column", "justifyContent": "flex-end"}),
        ], style={
            **CARD_STYLE,
            "display": "flex", "flexWrap": "wrap", "gap": "16px",
            "alignItems": "flex-end", "padding": "16px 20px", "marginBottom": "20px",
        }),

        # --- Outbreak alert placeholder (hidden until triggered) ----------
        html.Div(id="outbreak-alert-container"),

        # --- Prediction results -------------------------------------------
        html.Div(id="prediction-result-container"),

        # --- Gauge + Feature importance row --------------------------------
        html.Div([
            html.Div(
                dcc.Graph(id="gauge-chart", config={"displayModeBar": False},
                          style={"height": "320px"}),
                style={**CHART_CARD_STYLE, "flex": "1", "minWidth": "380px"},
            ),
            html.Div(
                dcc.Graph(id="feature-chart", config={"displayModeBar": False},
                          style={"height": "320px"}),
                style={**CHART_CARD_STYLE, "flex": "1", "minWidth": "380px"},
            ),
        ], style={"display": "flex", "gap": "16px", "flexWrap": "wrap"}),

        # --- Alert history table ------------------------------------------
        html.Div([
            html.H3("📋 Alert History Log", style={
                "fontSize": "16px", "fontWeight": "600", "color": TEXT_PRIMARY,
                "marginBottom": "12px",
            }),
            dash_table.DataTable(
                id="alert-log-table",
                columns=[
                    {"name": "Timestamp", "id": "timestamp"},
                    {"name": "Province", "id": "province"},
                    {"name": "District", "id": "district"},
                    {"name": "Probability", "id": "hotspot_probability"},
                    {"name": "Risk Level", "id": "risk_level"},
                ],
                data=[],
                style_header={
                    "backgroundColor": PRIMARY_LIGHT,
                    "fontWeight": "600",
                    "color": TEXT_PRIMARY,
                    "border": f"1px solid {BORDER}",
                    "fontFamily": FONT_FAMILY,
                    "fontSize": "13px",
                },
                style_cell={
                    "textAlign": "left",
                    "padding": "10px 14px",
                    "fontFamily": FONT_FAMILY,
                    "fontSize": "13px",
                    "border": f"1px solid {BORDER}",
                    "color": TEXT_PRIMARY,
                },
                style_data_conditional=[
                    {
                        "if": {"filter_query": '{risk_level} = "OUTBREAK ALERT"'},
                        "backgroundColor": "rgba(220, 38, 38, 0.08)",
                        "color": "#DC2626",
                        "fontWeight": "600",
                    },
                    {
                        "if": {"filter_query": '{risk_level} = "HIGH"'},
                        "backgroundColor": "rgba(255, 87, 34, 0.08)",
                        "color": "#E65100",
                        "fontWeight": "500",
                    },
                ],
                page_size=10,
                style_table={"overflowX": "auto"},
            ),
        ], style={**CARD_STYLE, "marginTop": "8px"}),
    ])


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def build_layout(df: pd.DataFrame) -> html.Div:
    """Construct and return the full dashboard layout."""
    return html.Div([
        # --- Header -------------------------------------------------------
        html.Div([
            html.H1("Disease Surveillance Analytics", style=HEADER_STYLE),
            html.P(
                "Infectious disease monitoring dashboard — powered by Plotly Dash",
                style=SUBHEADER_STYLE,
            ),
        ]),

        # --- Filters -------------------------------------------------------
        html.Div([
            create_year_filter(df),
            create_province_filter(df),
            create_district_filter(df),
            create_sex_filter(df),
            create_age_group_filter(df),
        ], style=FILTER_CONTAINER_STYLE),

        # --- KPI Row -------------------------------------------------------
        _kpi_row(),

        # --- Tabs -----------------------------------------------------------
        dcc.Tabs(id="main-tabs", value="overview", children=[
            dcc.Tab(label="Overview",       value="overview",
                    style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
            dcc.Tab(label="Geographic",     value="geographic",
                    style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
            dcc.Tab(label="Demographic",    value="demographic",
                    style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
            dcc.Tab(label="Surveillance",   value="surveillance",
                    style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
            dcc.Tab(label="🔮 Prediction",  value="prediction",
                    style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
        ], style={"marginBottom": "16px"}),

        html.Div(id="tab-content"),

        # --- Hidden store for passing df to prediction callback -----------
        dcc.Store(id="prediction-store"),

    ], style=PAGE_STYLE)
