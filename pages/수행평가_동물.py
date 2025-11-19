import streamlit as st
import pandas as pd
import altair as alt

# 풍선 애니메이션
st.balloons()

# 상단 제목 + 이모지
st.title("🐶🐱 경기도 시군별 반려동물 등록 현황 🐱🐶")
st.write("정확한 무지개 색상 그라데이션 + 풍선 효과 🎈")

# CSV 불러오기
df = pd.read_csv("dkdrlahWL.csv", encoding="cp949")

# 시군별 등록 동물 수 합계 계산
grouped = df.groupby("시군명")["등록동물수(마리)"].sum().reset_index()

# 무지개 색 배열
rainbow_colors = [
    "#FF0000",  # 빨강
    "#FF7F00",  # 주황
    "#FFFF00",  # 노랑
    "#00FF00",  # 초록
    "#0000FF",  # 파랑
    "#4B0082",  # 남색
    "#8B00FF"   # 보라
]

# Altair 막대그래프
chart = (
    alt.Chart(grouped)
    .mark_bar()
    .encode(
        x=alt.X("시군명:N", title="시군명", sort="-y"),
        y=alt.Y("등록동물수(마리):Q", title="등록 동물 수"),
        color=alt.Color(
            "등록동물수(마리):Q",
            scale=alt.Scale(
                range=rainbow_colors,
                reverse=True  # 가장 높은 값이 빨강
            ),
            legend=None
        ),
        tooltip=["시군명", "등록동물수(마리)"]
    )


st.altair_chart(chart, use_container_width=True)
