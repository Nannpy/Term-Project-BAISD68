"""
theme.py
========
Centralised design tokens and Plotly layout template for the dashboard.

Design language:
  • Bright / light background
  • Blue accent palette
  • Clean, minimalist typography (Inter from Google Fonts)
  • Rounded cards, subtle shadows
"""

import plotly.graph_objects as go
import plotly.io as pio

# ---------------------------------------------------------------------------
# Colour palette
# ---------------------------------------------------------------------------
PRIMARY       = "#1B6EF3"       # Bright blue
PRIMARY_LIGHT = "#E8F0FE"       # Very light blue tint
PRIMARY_DARK  = "#0D47A1"       # Deep blue for emphasis
ACCENT        = "#4FC3F7"       # Secondary accent
SUCCESS       = "#00C853"       # Green for positive indicators
DANGER        = "#FF1744"       # Red for negative indicators
WARNING       = "#FFD600"       # Yellow for warnings

BG_PAGE       = "#F5F7FA"       # Page background
BG_CARD       = "#FFFFFF"       # Card / panel background
TEXT_PRIMARY  = "#1E293B"       # Primary text
TEXT_SECONDARY= "#64748B"       # Secondary / muted text
BORDER        = "#E2E8F0"       # Card borders

CHART_COLORS  = [
    "#1B6EF3", "#4FC3F7", "#0D47A1", "#00C853",
    "#FF6D00", "#AA00FF", "#FF1744", "#FFD600",
    "#00BFA5", "#6D4C41",
]

# ---------------------------------------------------------------------------
# Typography & spacing
# ---------------------------------------------------------------------------
FONT_FAMILY  = "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
FONT_SIZE_SM = 12
FONT_SIZE_MD = 14
FONT_SIZE_LG = 18
FONT_SIZE_XL = 28

CARD_BORDER_RADIUS = "12px"
CARD_SHADOW        = "0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.06)"
CARD_PADDING       = "24px"

# ---------------------------------------------------------------------------
# Plotly template
# ---------------------------------------------------------------------------
_template = go.layout.Template()
_template.layout = go.Layout(
    font=dict(family=FONT_FAMILY, size=FONT_SIZE_MD, color=TEXT_PRIMARY),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    colorway=CHART_COLORS,
    margin=dict(l=48, r=24, t=56, b=40),
    title=dict(
        font=dict(size=FONT_SIZE_LG, color=TEXT_PRIMARY),
        x=0, xanchor="left",
    ),
    xaxis=dict(
        showgrid=True, gridcolor="#EEF2F6",
        zeroline=False, linecolor=BORDER,
    ),
    yaxis=dict(
        showgrid=True, gridcolor="#EEF2F6",
        zeroline=False, linecolor=BORDER,
    ),
    hoverlabel=dict(
        bgcolor=BG_CARD, font_size=FONT_SIZE_SM,
        font_family=FONT_FAMILY, bordercolor=BORDER,
    ),
    legend=dict(
        orientation="h", yanchor="bottom", y=1.02,
        xanchor="right", x=1,
    ),
)

pio.templates["surveillance"] = _template
pio.templates.default = "surveillance"

# ---------------------------------------------------------------------------
# CSS styles used by the Dash layout
# ---------------------------------------------------------------------------

EXTERNAL_STYLESHEETS = [
    "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
]

PAGE_STYLE = {
    "backgroundColor": BG_PAGE,
    "fontFamily": FONT_FAMILY,
    "minHeight": "100vh",
    "padding": "24px 32px",
}

CARD_STYLE = {
    "backgroundColor": BG_CARD,
    "borderRadius": CARD_BORDER_RADIUS,
    "boxShadow": CARD_SHADOW,
    "padding": CARD_PADDING,
    "border": f"1px solid {BORDER}",
}

KPI_CARD_STYLE = {
    **CARD_STYLE,
    "textAlign": "center",
    "padding": "20px 16px",
    "minWidth": "160px",
    "flex": "1",
}

KPI_VALUE_STYLE = {
    "fontSize": FONT_SIZE_XL,
    "fontWeight": "700",
    "color": PRIMARY,
    "margin": "8px 0 4px 0",
    "lineHeight": "1.1",
}

KPI_LABEL_STYLE = {
    "fontSize": FONT_SIZE_SM,
    "fontWeight": "500",
    "color": TEXT_SECONDARY,
    "textTransform": "uppercase",
    "letterSpacing": "0.5px",
}

CHART_CARD_STYLE = {
    **CARD_STYLE,
    "padding": "16px",
    "marginBottom": "16px",
}

FILTER_CONTAINER_STYLE = {
    **CARD_STYLE,
    "display": "flex",
    "flexWrap": "wrap",
    "gap": "16px",
    "alignItems": "flex-end",
    "padding": "16px 20px",
    "marginBottom": "20px",
}

FILTER_ITEM_STYLE = {
    "flex": "1",
    "minWidth": "160px",
}

HEADER_STYLE = {
    "fontSize": "26px",
    "fontWeight": "700",
    "color": TEXT_PRIMARY,
    "marginBottom": "4px",
}

SUBHEADER_STYLE = {
    "fontSize": FONT_SIZE_MD,
    "color": TEXT_SECONDARY,
    "marginBottom": "20px",
}

TAB_STYLE = {
    "padding": "12px 20px",
    "fontWeight": "500",
    "borderRadius": "8px 8px 0 0",
    "border": "none",
    "backgroundColor": "transparent",
    "color": TEXT_SECONDARY,
}

TAB_SELECTED_STYLE = {
    **TAB_STYLE,
    "backgroundColor": BG_CARD,
    "color": PRIMARY,
    "borderBottom": f"2px solid {PRIMARY}",
    "fontWeight": "600",
}

# ---------------------------------------------------------------------------
# Outbreak Early Warning styles
# ---------------------------------------------------------------------------

OUTBREAK_ALERT_STYLE = {
    "backgroundColor": "#DC2626",
    "color": "#FFFFFF",
    "borderRadius": CARD_BORDER_RADIUS,
    "padding": "24px 28px",
    "marginBottom": "20px",
    "boxShadow": "0 4px 14px rgba(220, 38, 38, 0.35)",
    "border": "2px solid #B91C1C",
    "textAlign": "center",
}

PREDICTION_CARD_STYLE = {
    **CARD_STYLE,
    "padding": "20px 24px",
    "marginBottom": "16px",
    "borderLeft": f"4px solid {PRIMARY}",
}

PREDICTION_BUTTON_STYLE = {
    "backgroundColor": PRIMARY,
    "color": "#FFFFFF",
    "border": "none",
    "borderRadius": "8px",
    "padding": "12px 32px",
    "fontSize": FONT_SIZE_MD,
    "fontWeight": "600",
    "cursor": "pointer",
    "fontFamily": FONT_FAMILY,
    "boxShadow": "0 2px 8px rgba(27, 110, 243, 0.3)",
    "transition": "all 0.2s ease",
}
