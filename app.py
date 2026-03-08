import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

# =========================
# Load Data
# =========================

df = pd.read_csv("Dengue_odpc4_2561.csv")
df.columns = df.columns.str.strip()

# แก้ error column
if 'datesick' in df.columns:
    df['datesick'] = pd.to_datetime(df['datesick'], errors='coerce')
else:
    df['datesick'] = pd.date_range(start="2023-01-01", periods=len(df))

if 'age' not in df.columns:
    df['age'] = 0

if 'gender' not in df.columns:
    df['gender'] = "Unknown"

if 'district' not in df.columns:
    df['district'] = "Unknown"

# =========================
# Data Summary
# =========================

total_cases = len(df)
male_cases = len(df[df['gender'] == 'ชาย'])
female_cases = len(df[df['gender'] == 'หญิง'])

gender_data = df['gender'].value_counts().reset_index()
gender_data.columns = ['gender','count']

district_data = df['district'].value_counts().head(10).reset_index()
district_data.columns = ['district','count']

date_data = df.groupby('datesick').size().reset_index(name="count")

# =========================
# Graphs
# =========================

fig_gender = px.pie(
    gender_data,
    names='gender',
    values='count',
    hole=0.5,
    title="Gender Distribution"
)

fig_age = px.histogram(
    df,
    x='age',
    nbins=30,
    title="Age Distribution"
)

fig_district = px.bar(
    district_data,
    x='district',
    y='count',
    title="Top District Cases",
    color='count'
)

fig_time = px.line(
    date_data,
    x='datesick',
    y='count',
    title="Dengue Cases Over Time"
)

# =========================
# App
# =========================

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY]
)

# =========================
# KPI Card Function
# =========================

def create_card(title,value,color):

    return dbc.Card(
        dbc.CardBody([
            html.H6(title,className="card-title"),
            html.H2(value,className="card-text")
        ]),
        style={
            "textAlign":"center",
            "backgroundColor":color,
            "borderRadius":"15px",
            "boxShadow":"0px 4px 15px rgba(0,0,0,0.4)"
        }
    )

# =========================
# Layout
# =========================

app.layout = dbc.Container([

    html.Br(),

    html.H1(
        "🦟 Dengue Fever Dashboard",
        style={
            "textAlign":"center",
            "fontWeight":"bold"
        }
    ),

    html.Hr(),

    # KPI Cards
    dbc.Row([

        dbc.Col(create_card("Total Patients",total_cases,"#2c3e50"),width=4),
        dbc.Col(create_card("Male Patients",male_cases,"#2980b9"),width=4),
        dbc.Col(create_card("Female Patients",female_cases,"#c0392b"),width=4),

    ],className="mb-4"),

    # Row 1
    dbc.Row([

        dbc.Col(
            dbc.Card(
                dcc.Graph(figure=fig_gender),
                style={"borderRadius":"15px"}
            ),
            width=6
        ),

        dbc.Col(
            dbc.Card(
                dcc.Graph(figure=fig_age),
                style={"borderRadius":"15px"}
            ),
            width=6
        )

    ],className="mb-4"),

    # Row 2
    dbc.Row([

        dbc.Col(
            dbc.Card(
                dcc.Graph(figure=fig_district),
                style={"borderRadius":"15px"}
            ),
            width=6
        ),

        dbc.Col(
            dbc.Card(
                dcc.Graph(figure=fig_time),
                style={"borderRadius":"15px"}
            ),
            width=6
        )

    ])

],fluid=True)

# =========================
# Run Server
# =========================

if __name__ == "__main__":
    app.run(debug=True)