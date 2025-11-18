# File: pages/metro_analysis.py
import streamlit as st
import pandas as pd
import plotly.express as px

# CSV is in root folder
DATA_PATH = "BONGSUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUN.csv"

st.title("🚇 2025년 10월 지하철 승하차 분석")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH, encoding="cp949")

df = load_data()

# Date selection (2025-10-01 ~ 2025-10-31 assumed)
available_dates = sorted(df["사용일자"].unique())
selected_date = st.selectbox("날짜를 선택하세요", available_dates)

# Filter by date
filtered_df = df[df["사용일자"] == selected_date]

# Line selection
available_lines = sorted(filtered_df["노선명"].unique())
selected_line = st.selectbox("호선을 선택하세요", available_lines)

# Filter by line
line_df = filtered_df[filtered_df["노선명"] == selected_line].copy()
line_df["총승하차"] = line_df["승차총승객수"] + line_df["하차총승객수"]
line_df = line_df.sort_values(by="총승하차", ascending=False)

# Color gradient
colors = ["red"] + px.colors.sequential.Blues[len(line_df)-1]

# Plotly bar chart
fig = px.bar(
    line_df,
    x="역명",
    y="총승하차",
    title=f"{selected_date} / {selected_line} 승하차 총계 Top 역",
    color=line_df.index,
    color_discrete_sequence=colors,
)

fig.update_layout(showlegend=False)

st.plotly_chart(fig, use_container_width=True)
