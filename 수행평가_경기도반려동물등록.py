import streamlit as st
import pandas as pd
import altair as alt

# -------------------------------
# 🎈 초기 효과: 풍선
# -------------------------------
st.balloons()

# -------------------------------
# 📘 CSV 불러오기
# -------------------------------
df = pd.read_csv("/mnt/data/dkdrlahWL.csv", encoding="cp949")

# 시군별 등록 동물 수 계산
grouped = df.groupby("시군명")["등록동물수(마리)"].sum().reset_index()

st.title("🐾 경기도 시군별 반려동물 등록 현황")
st.write("무지개 색상(빨 → 보) 그래프와 반려동물 추천 시스템")

# -------------------------------
# 🌈 무지개 그래프
# -------------------------------
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

# -------------------------------
# 🐶🐱 반려동물 추천 시스템
# -------------------------------
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

    # 질문 기반 추천 로직
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
    best_pet = max(scores, key=scores.get).strip()

    st.subheader(f"✨ 당신에게 어울리는 반려동물은 **{best_pet}**입니다!")

    # -------------------------------
    # 🖼️ 반려동물 이미지 (로컬 + Unsplash)
    # -------------------------------
    pet_images = {
        "강아지": "/mnt/data/갱얼쥐.jpg",
        "코브라": "/mnt/data/코브라띠.webp",

        # Streamlit에서 확실하게 뜨는 Unsplash CDN
        "고양이": "https://images.unsplash.com/photo-1518791841217-8f162f1e1131",
        "햄스터": "https://images.unsplash.com/photo-1558944351-c9c41341f95d",
        "기니피그": "https://images.unsplash.com/photo-1583511655826-a5c72c2afbec",
        "앵무새": "https://images.unsplash.com/photo-1501706362039-c06b2d715385"
    }

    fallback_image = "https://images.unsplash.com/photo-1518791841217-8f162f1e1131"
    image_url = pet_images.get(best_pet, fallback_image)

    st.image(image_url, caption=f"{best_pet} 사진", use_column_width=True)

    # 하트 효과
    st.snow()
    st.success("💖 반려동물을 사랑해주세요! 💖")

st.markdown("---")
st.write("더 많은 한국어 전용 AI는 https://gptonline.ai/ko/ 에서 확인하세요 😊")
