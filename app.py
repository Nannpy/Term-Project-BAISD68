import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np

# =========================
# Load Dataset
# =========================

df = pd.read_csv("Dengue_odpc4_2561.csv")
df.columns = df.columns.str.strip()

# =========================
# Fix Missing Columns
# =========================

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
# Summary Data
# =========================

total_cases = len(df)
male_cases = len(df[df['gender'] == 'ชาย'])
female_cases = len(df[df['gender'] == 'หญิง'])

gender_data = df['gender'].value_counts().reset_index()
gender_data.columns = ['gender', 'count']

district_data = df['district'].value_counts().head(10).reset_index()
district_data.columns = ['district', 'count']

date_data = df.groupby('datesick').size().reset_index(name='count')

# =========================
# Machine Learning
# =========================

def dengue_prediction(data):

    cases = data.groupby('datesick').size().reset_index(name='count')

    cases['date_num'] = cases['datesick'].map(pd.Timestamp.toordinal)

    X = cases[['date_num']]
    y = cases['count']

    model = LinearRegression()
    model.fit(X, y)

    # predict future
    future_days = 30
    last_date = cases['datesick'].max()

    future_dates = pd.date_range(last_date, periods=future_days)

    future_num = future_dates.map(pd.Timestamp.toordinal).values.reshape(-1,1)

    prediction = model.predict(future_num)

    future_df = pd.DataFrame({
        "datesick": future_dates,
        "predicted_cases": prediction
    })

    return cases, future_df


real_cases, predicted_cases = dengue_prediction(df)

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
    color='count',
    title="Top District Dengue Cases"
)

fig_time = px.line(
    date_data,
    x='datesick',
    y='count',
    title="Dengue Cases Over Time"
)

# ML Prediction Graph
fig_ml = px.line(
    real_cases,
    x="datesick",
    y="count",
    title="Dengue Cases Prediction (Machine Learning)"
)

fig_ml.add_scatter(
    x=predicted_cases["datesick"],
    y=predicted_cases["predicted_cases"],
    mode='lines',
    name="Prediction",
    line=dict(dash='dash')
)

# =========================
# App
# =========================

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY]
)

# =========================
# Card Function
# =========================

def create_card(title,value,color):

    return dbc.Card(
        dbc.CardBody([
            html.H5(title),
            html.H2(value)
        ]),
        style={
            "textAlign":"center",
            "backgroundColor":color,
            "borderRadius":"15px",
            "boxShadow":"0px 5px 20px rgba(0,0,0,0.4)"
        }
    )

# =========================
# Layout
# =========================

app.layout = dbc.Container([

    html.Br(),

    html.H1(
        "🦟 Dengue Fever Dashboard",
        style={"textAlign":"center","fontWeight":"bold"}
    ),

    html.Hr(),

    # KPI
    dbc.Row([

        dbc.Col(create_card("Total Patients",total_cases,"#2c3e50"),width=4),
        dbc.Col(create_card("Male Patients",male_cases,"#2980b9"),width=4),
        dbc.Col(create_card("Female Patients",female_cases,"#c0392b"),width=4),

    ],className="mb-4"),

    # Graph Row 1
    dbc.Row([

        dbc.Col(
            dbc.Card(dcc.Graph(figure=fig_gender)),
            width=6
        ),

        dbc.Col(
            dbc.Card(dcc.Graph(figure=fig_age)),
            width=6
        )

    ],className="mb-4"),

    # Graph Row 2
    dbc.Row([

        dbc.Col(
            dbc.Card(dcc.Graph(figure=fig_district)),
            width=6
        ),

        dbc.Col(
            dbc.Card(dcc.Graph(figure=fig_time)),
            width=6
        )

    ],className="mb-4"),

    # ML Graph
    dbc.Row([

        dbc.Col(
            dbc.Card(dcc.Graph(figure=fig_ml)),
            width=12
        )

    ])

],fluid=True)

# =========================
# Run Server
# =========================

if __name__ == "__main__":
    app.run(debug=True)