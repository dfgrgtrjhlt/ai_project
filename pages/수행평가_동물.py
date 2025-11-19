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

    st.subheader("🐾 나에게 맞는 반려동물 추천받기")

# 사용자 설문
size_pref = st.selectbox(
    "작고 귀여운 동물을 원하나요?",
    ["상관없음", "네"]
)

house_pref = st.selectbox(
    "집 크기가 작은 편인가요?",
    ["상관없음", "네"]
)

hair_pref = st.selectbox(
    "털 관리가 부담되나요?",
    ["상관없음", "네"]
)

active_pref = st.selectbox(
    "활발한 동물을 좋아하나요?",
    ["상관없음", "네"]
)

unique_pref = st.selectbox(
    "독특하거나 특별한 동물을 좋아하나요?",
    ["상관없음", "네"]
)

# 각 동물 기본 점수
scores = {
    "강아지": 0,
    "고양이": 0,
    "햄스터": 0,
    "기니피그": 0,
    "앵무새": 0,
    "코브라": 0
}

# 룰 기반 점수 부여
if size_pref == "네":
    scores["햄스터"] += 2
    scores["기니피그"] += 2
    scores["앵무새"] += 1

if house_pref == "네":
    scores["고양이"] += 1
    scores["햄스터"] += 2
    scores["기니피그"] += 2

if hair_pref == "네":
    scores["앵무새"] += 2
    scores["코브라"] += 2
    scores["햄스터"] += 1

if active_pref == "네":
    scores["강아지"] += 2
    scores["앵무새"] += 1

if unique_pref == "네":
    scores["코브라"] += 3
    scores["앵무새"] += 1

# 최종 추천
best_pet = max(scores, key=scores.get)

st.success(f"👉 당신에게 추천하는 반려동물은 **{best_pet}** 입니다!")
