import streamlit as st
import pandas as pd
import altair as alt

# CSV 불러오기
df = pd.read_csv("dkdrlahWL.csv", encoding="cp949")

# 시군별 등록 동물 수 합계 계산
grouped = df.groupby("시군명")["등록동물수(마리)"].sum().reset_index()

st.title("경기도 시군별 반려동물 등록 현황")
st.write("무지개 색상 그라데이션 적용 막대그래프")

# Rainbow Gradient Bar Chart
chart = (
    alt.Chart(grouped)
    .mark_bar()
    .encode(
        x=alt.X("시군명:N", title="시군명", sort="-y"),
        y=alt.Y("등록동물수(마리):Q", title="등록 동물 수"),
        color=alt.Color(
            "등록동물수(마리):Q",
            scale=alt.Scale(scheme="rainbow"),
            legend=None
        ),
        tooltip=["시군명", "등록동물수(마리)"]
    )
)

st.altair_chart(chart, use_container_width=True)
