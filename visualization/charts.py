"""
charts.py
=========
Reusable Plotly figure-factory functions for the surveillance dashboard.

Every function returns a ``plotly.graph_objects.Figure`` with titles, axis
labels, hover tooltips, and the shared "surveillance" template applied.

FUTURE AI EXTENSION:
---------------------
To visualise ML predictions (e.g. forecast lines, confidence intervals),
add new chart functions here that accept prediction DataFrames from
``ml.predictor.get_predictions()``.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from visualization.theme import (
    PRIMARY, ACCENT, DANGER, CHART_COLORS, FONT_FAMILY,
)

# ---------------------------------------------------------------------------
# Overview charts
# ---------------------------------------------------------------------------

def cases_over_time(df: pd.DataFrame) -> go.Figure:
    """Monthly case counts as an area chart."""
    if df.empty or "year_month" not in df.columns:
        return _empty_fig("Cases Over Time")
    agg = df.groupby("year_month").size().reset_index(name="cases")
    agg = agg.sort_values("year_month")
    fig = px.area(
        agg, x="year_month", y="cases",
        title="Cases Over Time",
        labels={"year_month": "Month", "cases": "Number of Cases"},
        color_discrete_sequence=[PRIMARY],
    )
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Cases: %{y:,}<extra></extra>",
        line=dict(width=2),
    )
    fig.update_layout(xaxis_tickangle=-45)
    return fig


def deaths_over_time(df: pd.DataFrame) -> go.Figure:
    """Monthly death counts as a line chart."""
    if df.empty or "year_month" not in df.columns:
        return _empty_fig("Deaths Over Time")
    deaths = df[df["death"] == 1]
    agg = deaths.groupby("year_month").size().reset_index(name="deaths")
    agg = agg.sort_values("year_month")
    fig = px.line(
        agg, x="year_month", y="deaths",
        title="Deaths Over Time",
        labels={"year_month": "Month", "deaths": "Number of Deaths"},
        color_discrete_sequence=[DANGER],
        markers=True,
    )
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Deaths: %{y:,}<extra></extra>",
    )
    fig.update_layout(xaxis_tickangle=-45)
    return fig


def weekly_case_trends(df: pd.DataFrame) -> go.Figure:
    """Weekly case counts aggregated across all years."""
    if df.empty or "week" not in df.columns:
        return _empty_fig("Weekly Case Trends")
    agg = df.groupby("week").size().reset_index(name="cases")
    agg = agg.sort_values("week")
    fig = px.bar(
        agg, x="week", y="cases",
        title="Weekly Case Trends (All Years)",
        labels={"week": "Week Number", "cases": "Number of Cases"},
        color_discrete_sequence=[ACCENT],
    )
    fig.update_traces(
        hovertemplate="Week %{x}<br>Cases: %{y:,}<extra></extra>",
    )
    return fig


# ---------------------------------------------------------------------------
# Geographic charts
# ---------------------------------------------------------------------------

def cases_by_province(df: pd.DataFrame) -> go.Figure:
    """Horizontal bar chart of cases per province."""
    if df.empty or "province" not in df.columns:
        return _empty_fig("Cases by Province")
    agg = df.groupby("province").size().reset_index(name="cases")
    agg = agg.sort_values("cases", ascending=True).tail(20)
    fig = px.bar(
        agg, x="cases", y="province", orientation="h",
        title="Top Provinces by Case Count",
        labels={"province": "Province", "cases": "Cases"},
        color_discrete_sequence=[PRIMARY],
    )
    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>Cases: %{x:,}<extra></extra>",
    )
    fig.update_layout(yaxis_title="", height=500)
    return fig


def cases_by_district(df: pd.DataFrame) -> go.Figure:
    """Top 20 districts by case count."""
    if df.empty or "district" not in df.columns:
        return _empty_fig("Cases by District")
    agg = df.groupby("district").size().reset_index(name="cases")
    agg = agg.sort_values("cases", ascending=True).tail(20)
    fig = px.bar(
        agg, x="cases", y="district", orientation="h",
        title="Top 20 Districts by Case Count",
        labels={"district": "District", "cases": "Cases"},
        color_discrete_sequence=[ACCENT],
    )
    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>Cases: %{x:,}<extra></extra>",
    )
    fig.update_layout(yaxis_title="", height=500)
    return fig


# ---------------------------------------------------------------------------
# Demographic charts
# ---------------------------------------------------------------------------

def age_distribution(df: pd.DataFrame) -> go.Figure:
    """Histogram of raw age in years."""
    if df.empty or "agey" not in df.columns:
        return _empty_fig("Age Distribution")
    fig = px.histogram(
        df, x="agey", nbins=40,
        title="Age Distribution",
        labels={"agey": "Age (years)", "count": "Count"},
        color_discrete_sequence=[PRIMARY],
    )
    fig.update_traces(
        hovertemplate="Age: %{x}<br>Count: %{y:,}<extra></extra>",
    )
    fig.update_layout(bargap=0.05)
    return fig


def age_group_distribution(df: pd.DataFrame) -> go.Figure:
    """Bar chart of age groups."""
    if df.empty or "age_group" not in df.columns:
        return _empty_fig("Cases by Age Group")
    agg = df.groupby("age_group", observed=False).size().reset_index(name="cases")
    fig = px.bar(
        agg, x="age_group", y="cases",
        title="Cases by Age Group",
        labels={"age_group": "Age Group", "cases": "Cases"},
        color_discrete_sequence=[PRIMARY],
    )
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Cases: %{y:,}<extra></extra>",
    )
    return fig


def sex_distribution(df: pd.DataFrame) -> go.Figure:
    """Donut chart of sex distribution."""
    if df.empty or "Sex_en" not in df.columns:
        return _empty_fig("Sex Distribution")
    agg = df.groupby("Sex_en").size().reset_index(name="cases")
    fig = px.pie(
        agg, values="cases", names="Sex_en",
        title="Sex Distribution",
        hole=0.5,
        color_discrete_sequence=[PRIMARY, ACCENT, "#94A3B8"],
    )
    fig.update_traces(
        hovertemplate="<b>%{label}</b><br>Cases: %{value:,}<br>%{percent}<extra></extra>",
        textinfo="label+percent",
    )
    return fig


def occupation_distribution(df: pd.DataFrame) -> go.Figure:
    """Top 10 occupations by case count."""
    if df.empty or "occupat" not in df.columns:
        return _empty_fig("Cases by Occupation")
    agg = df.groupby("occupat").size().reset_index(name="cases")
    agg = agg.sort_values("cases", ascending=True).tail(10)
    fig = px.bar(
        agg, x="cases", y="occupat", orientation="h",
        title="Top 10 Occupations",
        labels={"occupat": "Occupation", "cases": "Cases"},
        color_discrete_sequence=[PRIMARY],
    )
    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>Cases: %{x:,}<extra></extra>",
    )
    fig.update_layout(yaxis_title="", height=400)
    return fig


# ---------------------------------------------------------------------------
# Surveillance / Delay charts
# ---------------------------------------------------------------------------

def reporting_delay_distribution(df: pd.DataFrame) -> go.Figure:
    """Histogram of reporting delays (days)."""
    if df.empty or "reporting_delay" not in df.columns:
        return _empty_fig("Reporting Delay Distribution")
    filtered = df[df["reporting_delay"] >= 0]
    fig = px.histogram(
        filtered, x="reporting_delay", nbins=50,
        title="Reporting Delay Distribution",
        labels={"reporting_delay": "Reporting Delay (days)", "count": "Count"},
        color_discrete_sequence=[PRIMARY],
    )
    fig.update_traces(
        hovertemplate="Delay: %{x} days<br>Count: %{y:,}<extra></extra>",
    )
    fig.update_layout(bargap=0.05)
    return fig


def diagnosis_delay_distribution(df: pd.DataFrame) -> go.Figure:
    """Histogram of diagnosis delays (days_to_define)."""
    if df.empty or "diagnosis_delay" not in df.columns:
        return _empty_fig("Diagnosis Delay Distribution")
    filtered = df[df["diagnosis_delay"] >= 0]
    fig = px.histogram(
        filtered, x="diagnosis_delay", nbins=50,
        title="Diagnosis Delay Distribution",
        labels={"diagnosis_delay": "Diagnosis Delay (days)", "count": "Count"},
        color_discrete_sequence=[ACCENT],
    )
    fig.update_traces(
        hovertemplate="Delay: %{x} days<br>Count: %{y:,}<extra></extra>",
    )
    fig.update_layout(bargap=0.05)
    return fig


def avg_reporting_delay_by_province(df: pd.DataFrame) -> go.Figure:
    """Average reporting delay per province."""
    if df.empty or "reporting_delay" not in df.columns:
        return _empty_fig("Avg Reporting Delay by Province")
    agg = (
        df[df["reporting_delay"] >= 0]
        .groupby("province")["reporting_delay"]
        .mean()
        .reset_index(name="avg_delay")
        .sort_values("avg_delay", ascending=True)
        .tail(20)
    )
    agg["avg_delay"] = agg["avg_delay"].round(1)
    fig = px.bar(
        agg, x="avg_delay", y="province", orientation="h",
        title="Avg Reporting Delay by Province (Top 20)",
        labels={"province": "Province", "avg_delay": "Avg Delay (days)"},
        color_discrete_sequence=[DANGER],
    )
    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>Avg Delay: %{x:.1f} days<extra></extra>",
    )
    fig.update_layout(yaxis_title="", height=500)
    return fig


# ---------------------------------------------------------------------------
# Prediction / Early Warning charts
# ---------------------------------------------------------------------------

def hotspot_gauge(probability: float) -> go.Figure:
    """Gauge chart for hotspot probability with dynamic color bands.

    Green → Low risk, Orange → Medium, Red → High, Dark-Red → Outbreak.
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=probability * 100,
        number={"suffix": "%", "font": {"size": 42, "family": FONT_FAMILY}},
        title={"text": "Hotspot Probability", "font": {"size": 18, "family": FONT_FAMILY}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#CBD5E1"},
            "bar": {"color": _gauge_bar_color(probability)},
            "bgcolor": "#F1F5F9",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 40],   "color": "rgba(0, 200, 83, 0.15)"},
                {"range": [40, 70],  "color": "rgba(255, 152, 0, 0.15)"},
                {"range": [70, 80],  "color": "rgba(255, 87, 34, 0.15)"},
                {"range": [80, 100], "color": "rgba(220, 38, 38, 0.15)"},
            ],
            "threshold": {
                "line": {"color": "#DC2626", "width": 3},
                "thickness": 0.8,
                "value": 80,
            },
        },
    ))
    fig.update_layout(height=300, margin=dict(t=60, b=20, l=40, r=40))
    return fig


def _gauge_bar_color(probability: float) -> str:
    """Return the gauge bar color based on probability value."""
    if probability >= 0.8:
        return "#DC2626"    # dark red — outbreak
    if probability >= 0.7:
        return "#FF5722"    # red — high
    if probability >= 0.4:
        return "#FF9800"    # orange — medium
    return "#00C853"        # green — low


def feature_importance_chart(feature_scores: dict) -> go.Figure:
    """Horizontal bar chart showing feature importance scores."""
    if not feature_scores:
        return _empty_fig("Feature Importance")

    sorted_items = sorted(feature_scores.items(), key=lambda x: x[1])
    names = [item[0] for item in sorted_items]
    values = [item[1] for item in sorted_items]

    fig = go.Figure(go.Bar(
        x=values, y=names, orientation="h",
        marker=dict(
            color=values,
            colorscale=[[0, ACCENT], [0.5, PRIMARY], [1, DANGER]],
            line=dict(width=0),
        ),
        hovertemplate="<b>%{y}</b><br>Score: %{x:.3f}<extra></extra>",
    ))
    fig.update_layout(
        title="Feature Importance",
        xaxis_title="Importance Score",
        yaxis_title="",
        height=320,
        margin=dict(l=140, r=24, t=56, b=40),
    )
    return fig


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _empty_fig(title: str) -> go.Figure:
    """Return an empty figure with a 'No data' annotation."""
    fig = go.Figure()
    fig.update_layout(
        title=title,
        annotations=[dict(
            text="No data available", showarrow=False,
            xref="paper", yref="paper", x=0.5, y=0.5,
            font=dict(size=16, color="#94A3B8"),
        )],
    )
    return fig
