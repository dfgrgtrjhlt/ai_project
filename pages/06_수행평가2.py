import streamlit as st
import pandas as pd
import altair as alt

# ---------------------------------------
# 📌 GitHub RAW XLSX URL (여기에 본인 주소 넣기)
# ---------------------------------------
GITHUB_XLSX_URL = "https://raw.githubusercontent.com/your-id/your-repo/main/반려동물등록현황 (1).csv.xlsx"

# ---------------------------------------
# 📘 GitHub XLSX 불러오기 함수
# ---------------------------------------
def read_xlsx_from_github(url):
    return pd.read_excel(url)

# ---------------------------------------
# 🎈 풍선 효과
# ---------------------------------------
st.balloons()

st.title("🐾 경기도 시군별 반려동물 등록 현황 (XLSX 자동 불러오기 버전)")
st.write("GitHub의 Excel 파일을 자동으로 불러와 시각화합니다.")

# ---------------------------------------
# 📁 데이터 로드
# ---------------------------------------
try:
    df = read_xlsx_from_github(GITHUB_XLSX_URL)
    st.success("✅ GitHub에서 XLSX 파일을 자동으로 불러왔습니다!")
except Exception as e:
    st.error(f"❌ XLSX 파일을 불러오지 못했습니다: {e}")
    st.stop()

# ---------------------------------------
# 📊 시군별 등록 동물 수 집계
# ---------------------------------------
grouped = df.groupby("시군명")["등록동물수(마리)"].sum().reset_index()

st.subheader("🌈 시군별 반려동물 등록 수 그래프")

rainbow_colors = ["#ff0000", "#ff7f00", "#ffff00", "#00ff00", "#0000ff", "#8b00ff"]
grouped = grouped.sort_values("등록동물수(마리)", ascending=False)
grouped["color"] = rainbow_colors * (len(grouped) // len(rainbow_colors) + 1)

chart = (
    alt.Chart(grouped)
    .mark_bar()
    .encode(
        x=alt.X("시군명:N", title="시군명", sort="-y"),
        y=alt.Y("등록동물수(마리):Q", title="등록 동물 수"),
        color=alt.Color("color:N", scale=None),
        tooltip=["시군명", "등록동물수(마리)"]
    )
)

st.altair_chart(chart, use_container_width=True)

st.markdown("---")

# ---------------------------------------
# 🐶 반려동물 추천 시스템
# ---------------------------------------
st.header("💡 반려동물 추천받기")

q1 = st.radio("1. 집 평수는 어떤가요?", ["좁음", "보통", "넓음"])
q2 = st.radio("2. 활동량을 얼마나 원하나요?", ["적음", "보통", "많음"])
q3 = st.radio("3. 털 관리가 귀찮나요?", ["예", "아니오"])
q4 = st.radio("4. 조용한 동물이 좋나요?", ["예", "아니오"])

if st.button("반려동물 추천 받기 💖"):

    scores = {
        "강아지": 0,
        "고양이": 0,
        "햄스터": 0,
        "기니피그": 0,
        "앵무새": 0,
        "코브라": 0
    }

    # 점수 계산
    if q1 == "좁음":
        scores["햄스터"] += 2
        scores["기니피그"] += 2
        scores["코브라"] += 1
    elif q1 == "보통":
        scores["고양이"] += 2
        scores["앵무새"] += 1
    else:
        scores["강아지"] += 3
        scores["앵무새"] += 1

    if q2 == "적음":
        scores["고양이"] += 2
        scores["햄스터"] += 1
        scores["기니피그"] += 1
    elif q2 == "보통":
        scores["앵무새"] += 2
        scores["고양이"] += 1
    else:
        scores["강아지"] += 3
        scores["앵무새"] += 2

    if q3 == "예":
        scores["햄스터"] += 2
        scores["기니피그"] += 2
        scores["코브라"] += 3
    else:
        scores["강아지"] += 2
        scores["고양이"] += 2

    if q4 == "예":
        scores["햄스터"] += 2
        scores["코브라"] += 2
        scores["기니피그"] += 1
    else:
        scores["강아지"] += 2
        scores["앵무새"] += 2

    # 결과
    best_pet = max(scores, key=scores.get)
    st.subheader(f"✨ 당신에게 어울리는 반려동물은 **{best_pet}** 입니다!")

    # 이미지 표시
    pet_images = {
        "강아지": "https://cdn.pixabay.com/photo/2014/04/02/10/56/dog-303604_1280.png",
        "고양이": "https://cdn.pixabay.com/photo/2017/11/09/21/41/cat-2934720_1280.png",
        "햄스터": "https://cdn.pixabay.com/photo/2016/05/24/18/44/hamster-1418139_1280.png",
        "기니피그": "https://cdn.pixabay.com/photo/2017/07/27/22/09/guinea-pig-2545929_1280.png",
        "앵무새": "https://cdn.pixabay.com/photo/2017/09/25/13/12/parrot-2785276_1280.png",
        "코브라": "https://cdn.pixabay.com/photo/2014/12/21/23/36/snake-575304_1280.png"
    }

    st.image(pet_images.get(best_pet, ""), width=250)

    st.snow()
    st.success("💖 반려동물을 사랑해주세요! 💖")

st.markdown("---")
st.write("더 많은 한국어 AI는 https://gptonline.ai/ko/ 에서 확인하세요 😊")
