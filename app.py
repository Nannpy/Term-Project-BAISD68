import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px

# ---------------------------
# โหลดข้อมูล
# ---------------------------
df = pd.read_csv(
    "Dengue_odpc4_2561.csv",
    delim_whitespace=True,
    encoding="utf-8"
)

# แปลงวันที่
df['datesick'] = pd.to_datetime(df['datesick'], errors='coerce')

# ---------------------------
# เตรียมข้อมูล
# ---------------------------

# เพศ
sex_count = df['Sex'].value_counts().reset_index()
sex_count.columns = ['Sex', 'count']

# อายุ
age_df = df[df['agey'].notna()]

# อำเภอ
district_count = df['district'].value_counts().reset_index()
district_count.columns = ['district', 'count']

# ผู้ป่วยตามวัน
date_count = df.groupby('datesick').size().reset_index(name='count')

# ---------------------------
# สร้างกราฟ
# ---------------------------

fig_sex = px.bar(
    sex_count,
    x="Sex",
    y="count",
    title="จำนวนผู้ป่วยตามเพศ"
)

fig_age = px.histogram(
    age_df,
    x="agey",
    nbins=30,
    title="การกระจายอายุผู้ป่วย"
)

fig_district = px.bar(
    district_count,
    x="district",
    y="count",
    title="จำนวนผู้ป่วยตามอำเภอ"
)

fig_date = px.line(
    date_count,
    x="datesick",
    y="count",
    title="จำนวนผู้ป่วยตามวัน"
)

# ---------------------------
# สร้าง Dash App
# ---------------------------

app = Dash(__name__)

app.layout = html.Div([

    html.H1(
        "Dengue Fever Dashboard",
        style={
            'textAlign': 'center',
            'color': '#2c3e50'
        }
    ),

    html.H3(
        f"Total Patients: {len(df)}",
        style={'textAlign': 'center'}
    ),

    dcc.Graph(
        figure=fig_sex
    ),

    dcc.Graph(
        figure=fig_age
    ),

    dcc.Graph(
        figure=fig_district
    ),

    dcc.Graph(
        figure=fig_date
    )

])

# ---------------------------

if __name__ == "__main__":
    app.run(debug=True)