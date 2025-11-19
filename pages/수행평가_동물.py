import streamlit as st
import pandas as pd
import altair as alt

# --------------------------------
# ❤️ 커스텀 하트 이펙트 함수
# --------------------------------
def heart_effect():
    heart_css = """
    <style>
    .heart {
        position: fixed;
        bottom: -50px;
        font-size: 40px;
        animation: floatUp 4s ease-in-out infinite;
        z-index: 9999;
    }

    @keyframes floatUp {
        0% { bottom: -50px; opacity: 1; left: 50%; }
        100% { bottom: 100%; opacity: 0; left: 55%; }
    }
    </style>

    <div class="heart">💖</div>
    <div class="heart" style="left:40%;">💕</div>
    <div class="heart" style="left:60%;">💗</div>
    <div class="heart" style="left:45%;">💞</div>
    """
    st.markdown(heart_css, unsafe_allow_html=True)


# --------------------------------
# 🎨 페이지 효과 선택
# --------------------------------
effect = st.selectbox(
    "페이지 효과를 선택하세요 🎨",
    ["풍선 효과", "눈(스노우) 효과", "효과 없음"]
)

if effect == "풍선 효과":
    st.balloons()
elif effect == "눈(스노우) 효과":
    st.snow()

# --------------------------------
# 🐶🐱 제목
# --------------------------------
st.title("🐶🐱 경기도 시군별 반려동물 등록 현황 시각화 🐱🐶")
st.write("무지개 색 그래프 + 반려동물 추천 + 사진 + 하트 이펙트 💖")

# --------------------------------
# 📄 CSV 읽기
# --------------------------------
df = pd.read_csv("dkdrlahWL.csv", encoding="cp949")
grouped = df.groupby("시군명")["등록동물수(마리)"].sum().reset_index()

# --------------------------------
# 🌈 무지개 색상
# --------------------------------
rainbow_colors = [
    "#FF0000", "#FF7F00", "#FFFF00",
    "#00FF00", "#0000FF", "#4B0082", "#8B00FF"
]

# --------------------------------
# 📊 그래프
# --------------------------------
chart = (
    alt.Chart(grouped)
    .mark_bar()
    .encode(
        x=alt.X("시군명:N", title="시군명", sort="-y"),
        y=alt.Y("등록동물수(마리):Q", title="등록 동물 수"),
        color=alt.Color(
            "등록동물수(마리):Q",
            scale=alt.Scale(range=rainbow_colors, reverse=True),
            legend=None
        ),
        tooltip=["시군명", "등록동물수(마리)"]
    )
)

st.altair_chart(chart, use_container_width=True)

# --------------------------------
# 🐾 추천 시스템 UI
# --------------------------------
st.subheader("🐾 나에게 맞는 반려동물 추천받기")

size_pref = st.selectbox("작고 귀여운 동물을 원하나요?", ["상관없음", "네"])
house_pref = st.selectbox("집 크기가 작은 편인가요?", ["상관없음", "네"])
hair_pref = st.selectbox("털 관리가 부담되나요?", ["상관없음", "네"])
active_pref = st.selectbox("활발한 동물을 좋아하나요?", ["상관없음", "네"])
unique_pref = st.selectbox("독특하거나 특별한 동물을 좋아하나요?", ["상관없음", "네"])

scores = {"강아지":0, "고양이":0, "햄스터":0, "기니피그":0, "앵무새":0, "코브라":0}

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

best_pet = max(scores, key=scores.get)

st.success(f"🎉 당신에게 추천하는 반려동물은 **{best_pet}** 입니다!")



# 이미지를 표시하는 순간 💖 하트 효과 실행
heart_effect()

st.image(pet_images[best_pet], caption=f"{best_pet} 사진", use_column_width=True)
