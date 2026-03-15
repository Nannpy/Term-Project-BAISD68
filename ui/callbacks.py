"""
callbacks.py
============
Dash callbacks that wire filters → KPI updates and tab switching → chart
rendering, plus the Prediction tab with outbreak early warning system.
"""

from dash import Input, Output, State, callback, html, dcc, no_update
import pandas as pd

from core import kpi_engine
from visualization import charts
from ui.filters import apply_filters
from visualization.theme import (
    CHART_CARD_STYLE, CARD_STYLE, PREDICTION_CARD_STYLE,
    OUTBREAK_ALERT_STYLE, TEXT_PRIMARY, TEXT_SECONDARY,
    PRIMARY, DANGER, SUCCESS, ACCENT, FONT_FAMILY, BORDER,
)
from ml.outbreak_warning import predict_hotspot, log_alert, get_alert_log
from ml.reporting_lag import predict_lag


def register_callbacks(app, df: pd.DataFrame):
    """Register all Dash callbacks against the given *app* and *df*."""

    # ---- helper: build tab content from figures --------------------------
    def _wrap(fig, graph_id, h=380):
        return html.Div(
            dcc.Graph(id=graph_id, figure=fig,
                      config={"displayModeBar": False},
                      style={"height": f"{h}px"}),
            style={**CHART_CARD_STYLE, "flex": "1", "minWidth": "400px"},
        )

    def _row(*children):
        return html.Div(list(children), style={
            "display": "flex", "gap": "16px", "flexWrap": "wrap",
        })

    # ---- main callback ---------------------------------------------------
    @app.callback(
        # KPI outputs
        Output("kpi-total-cases",  "children"),
        Output("kpi-total-deaths", "children"),
        Output("kpi-cfr",          "children"),
        Output("kpi-avg-age",      "children"),
        Output("kpi-mf-ratio",     "children"),
        # Tab content
        Output("tab-content",      "children"),
        # Inputs
        Input("filter-year",       "value"),
        Input("filter-province",   "value"),
        Input("filter-district",   "value"),
        Input("filter-sex",        "value"),
        Input("filter-age-group",  "value"),
        Input("main-tabs",         "value"),
    )
    def update_dashboard(year, province, district, sex, age_group, active_tab):
        # Apply filters
        filtered = apply_filters(
            df, year=year, province=province,
            district=district, sex=sex, age_group=age_group,
        )

        # --- KPIs ---------------------------------------------------------
        kpis = kpi_engine.compute_all(filtered)
        kpi_cases  = f"{kpis['total_cases']:,}"
        kpi_deaths = f"{kpis['total_deaths']:,}"
        kpi_cfr    = f"{kpis['cfr']}%"
        kpi_age    = f"{kpis['avg_age']}"
        kpi_mf     = kpis["mf_ratio"]

        # --- Tab content --------------------------------------------------
        if active_tab == "overview":
            content = html.Div([
                _row(
                    _wrap(charts.cases_over_time(filtered), "g-cases-time"),
                    _wrap(charts.deaths_over_time(filtered), "g-deaths-time"),
                ),
                _row(
                    _wrap(charts.weekly_case_trends(filtered), "g-weekly"),
                ),
            ])

        elif active_tab == "geographic":
            content = html.Div([
                _row(
                    _wrap(charts.cases_by_province(filtered), "g-province", h=500),
                    _wrap(charts.cases_by_district(filtered), "g-district", h=500),
                ),
            ])

        elif active_tab == "demographic":
            content = html.Div([
                _row(
                    _wrap(charts.age_distribution(filtered), "g-age-dist"),
                    _wrap(charts.sex_distribution(filtered), "g-sex-dist"),
                ),
                _row(
                    _wrap(charts.age_group_distribution(filtered), "g-age-grp"),
                    _wrap(charts.occupation_distribution(filtered), "g-occup", h=400),
                ),
            ])

        elif active_tab == "surveillance":
            content = html.Div([
                _row(
                    _wrap(charts.reporting_delay_distribution(filtered), "g-rpt-delay"),
                    _wrap(charts.diagnosis_delay_distribution(filtered), "g-diag-delay"),
                ),
                _row(
                    _wrap(charts.avg_reporting_delay_by_province(filtered), "g-delay-prov", h=500),
                ),
            ])

        elif active_tab == "prediction":
            # Import here to use the layout helper
            from ui.layout import _tab_prediction
            content = _tab_prediction(df)

        else:
            content = html.Div("Select a tab.")

        return kpi_cases, kpi_deaths, kpi_cfr, kpi_age, kpi_mf, content

    # ---- prediction callback ---------------------------------------------
    @app.callback(
        Output("outbreak-alert-container", "children"),
        Output("prediction-result-container", "children"),
        Output("gauge-chart", "figure"),
        Output("feature-chart", "figure"),
        Output("alert-log-table", "data"),
        Input("btn-predict", "n_clicks"),
        State("pred-province", "value"),
        State("pred-district", "value"),
        prevent_initial_call=True,
    )
    def run_prediction(n_clicks, province, district):
        if not n_clicks:
            return no_update, no_update, no_update, no_update, no_update

        # --- Run hotspot prediction ---------------------------------------
        result = predict_hotspot(df, province=province, district=district)
        prob = result["probability"]
        risk = result["risk_level"]
        features = result["feature_scores"]
        model_type = result["model_type"]

        # --- Run reporting lag prediction ---------------------------------
        lag_result = predict_lag(df, province=province, district=district)
        predicted_lag = lag_result["predicted_lag_days"]
        lag_model_type = lag_result["model_type"]

        # --- Log the alert ------------------------------------------------
        log_alert(province, district, prob)

        # --- Build outbreak alert card (only if ≥ 0.80) -------------------
        if prob >= 0.80:
            alert_card = html.Div([
                html.Div("⚠️", style={
                    "fontSize": "48px", "marginBottom": "8px",
                }),
                html.H2("OUTBREAK WARNING", style={
                    "fontSize": "24px", "fontWeight": "700",
                    "margin": "0 0 12px 0", "letterSpacing": "1px",
                    "textTransform": "uppercase",
                }),
                html.P([
                    "High outbreak risk detected",
                    html.Br(),
                    f"in {district or 'selected area'}, {province or 'all provinces'}.",
                ], style={
                    "fontSize": "16px", "fontWeight": "500",
                    "margin": "0 0 8px 0", "lineHeight": "1.5",
                }),
                html.P(
                    f"Probability: {prob:.2%}",
                    style={
                        "fontSize": "20px", "fontWeight": "700",
                        "margin": "8px 0 4px 0",
                    },
                ),
                html.P(
                    "Immediate surveillance action recommended.",
                    style={
                        "fontSize": "14px", "fontWeight": "400",
                        "opacity": "0.9", "marginTop": "4px",
                    },
                ),
            ], style=OUTBREAK_ALERT_STYLE)
        else:
            alert_card = html.Div()  # empty — no alert

        # --- Build prediction result card ---------------------------------
        risk_colors = {
            "LOW": SUCCESS,
            "MEDIUM": "#FF9800",
            "HIGH": "#FF5722",
            "OUTBREAK ALERT": DANGER,
        }
        risk_color = risk_colors.get(risk, PRIMARY)
        risk_icons = {
            "LOW": "✅",
            "MEDIUM": "🟡",
            "HIGH": "🟠",
            "OUTBREAK ALERT": "🔴",
        }
        risk_icon = risk_icons.get(risk, "ℹ️")

        result_card = html.Div([
            html.Div([
                html.Div([
                    html.Span(risk_icon, style={"fontSize": "32px", "marginRight": "12px"}),
                    html.Div([
                        html.Div("Prediction Result", style={
                            "fontSize": "12px", "fontWeight": "600",
                            "color": TEXT_SECONDARY, "textTransform": "uppercase",
                            "letterSpacing": "0.5px", "marginBottom": "4px",
                        }),
                        html.Div(f"Risk Level: {risk}", style={
                            "fontSize": "22px", "fontWeight": "700",
                            "color": risk_color,
                        }),
                    ]),
                ], style={"display": "flex", "alignItems": "center"}),

                html.Div([
                    html.Div([
                        html.Span("Province: ", style={"color": TEXT_SECONDARY, "fontWeight": "500"}),
                        html.Span(province or "All", style={"fontWeight": "600"}),
                    ], style={"marginBottom": "4px", "fontSize": "14px"}),
                    html.Div([
                        html.Span("District: ", style={"color": TEXT_SECONDARY, "fontWeight": "500"}),
                        html.Span(district or "All", style={"fontWeight": "600"}),
                    ], style={"marginBottom": "4px", "fontSize": "14px"}),
                    html.Div([
                        html.Span("Hotspot Probability: ", style={"color": TEXT_SECONDARY, "fontWeight": "500"}),
                        html.Span(f"{prob:.2%}", style={"fontWeight": "700", "color": risk_color}),
                    ], style={"marginBottom": "4px", "fontSize": "14px"}),
                    html.Div([
                        html.Span("Predicted Reporting Lag: ", style={"color": TEXT_SECONDARY, "fontWeight": "500"}),
                        html.Span(f"{predicted_lag:.1f} days", style={"fontWeight": "700", "color": PRIMARY}),
                    ], style={"marginBottom": "4px", "fontSize": "14px"}),
                    html.Div([
                        html.Span("Models: ", style={"color": TEXT_SECONDARY, "fontWeight": "500"}),
                        html.Span(f"Hotspot ({model_type}), Lag ({lag_model_type})", style={
                            "fontWeight": "500", "fontStyle": "italic",
                        }),
                    ], style={"fontSize": "13px"}),
                ], style={"marginTop": "12px"}),
            ]),
        ], style={
            **PREDICTION_CARD_STYLE,
            "borderLeftColor": risk_color,
        })

        # --- Build gauge and feature charts --------------------------------
        gauge_fig = charts.hotspot_gauge(prob)
        feat_fig = charts.feature_importance_chart(features)

        # --- Alert log table data -----------------------------------------
        log_data = get_alert_log()

        return alert_card, result_card, gauge_fig, feat_fig, log_data
