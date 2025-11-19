import streamlit as st
import pandas as pd
import altair as alt

# -------------------------------------------------
# 🎈 앱 시작 시 자동 풍선 효과 (한 번만)
# -------------------------------------------------
if "balloon_shown" not in st.session_state:
    st.session_state.balloon_shown = True
    st.balloons()


# -------------------------------------------------
# 💖 커스텀 하트 이펙트 정의
# -------------------------------------------------
def heart_effect():
    heart_css = """
    <style>
    .heart {
        position: fixed;
        bottom: -40px;
        font-size: 40px;
        animation: floatUp 4s ease-in-out infinite;
        z-index: 999999;
        pointer-events: none;
    }

    @keyframes floatUp {
        0% { bottom: -40px; opacity: 1; }
        100% { bottom: 100%; opacity: 0; }
    }
    </style>
    <div class="heart" style="left:45%;">💖</div>
    <div class="heart" style="left:50%;">💕</div>
    <div class="heart" style="left:55%;">💗</div>
    <div class="heart" style="left:40%;">💞</div>
    <div class="heart" style="left:60%;">💘</div>
    """
    st.markdown(heart_css, unsafe_allow_html=True)


# -------------------------------------------------
# 🐶🐱 제목
# -------------------------------------------------
st.title("🐶🐱 경기도 시군별 반려동물 등록 현황 시각화 🐱🐶")
st.write("무지개 색 막대그래프 + 동물 추천 + 눈·하트 효과 🌈❄️💖")


# -------------------------------------------------
# 📄 CSV 불러오기
# -------------------------------------------------
df = pd.read_csv("dkdrlahWL.csv", encoding="cp949")
grouped = df.groupby("시군명")["등록동물수(마리)"].sum().reset_index()


# -------------------------------------------------
# 🌈 무지개 색상 정의
# -------------------------------------------------
rainbow_colors = [
    "#FF0000", "#FF7F00", "#FFFF00",
    "#00FF00", "#0000FF", "#4B0082", "#8B00FF"
]


# -------------------------------------------------
# 📊 그래프 출력
# -------------------------------------------------
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


# -------------------------------------------------
# 🐾 반려동물 추천 시스템
# -------------------------------------------------
st.subheader("🐾 나에게 맞는 반려동물 추천받기")

size_pref = st.selectbox("작고 귀여운 동물을 원하나요?", ["상관없음", "네"])
house_pref = st.selectbox("집 크기가 작은 편인가요?", ["상관없음", "네"])
hair_pref = st.selectbox("털 관리가 부담되나요?", ["상관없음", "네"])
active_pref = st.selectbox("활발한 동물을 좋아하나요?", ["상관없음", "네"])
unique_pref = st.selectbox("독특하거나 특별한 동물을 좋아하나요?", ["상관없음", "네"])

scores = {"강아지": 0, "고양이": 0, "햄스터": 0, "기니피그": 0, "앵무새": 0, "코브라": 0}

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

best_pet = max(scores, key=scores.get).strip()


# -------------------------------------------------
# 🎉 추천 결과 출력 + 효과 실행
# -------------------------------------------------
st.success(f"🎉 당신에게 추천하는 반려동물은 **{best_pet}** 입니다!")

# 눈 + 하트 효과
st.snow()
heart_effect()


# -------------------------------------------------
# 🖼 추천 동물 이미지 안전 출력
# -------------------------------------------------
pet_images = {
    "강아지": "https://cdn.pixabay.com/photo/2017/09/25/13/12/dog-2785074_1280.jpg",
    "고양이": "https://cdn.pixabay.com/photo/2017/11/09/21/41/cat-2934720_1280.jpg",
    "햄스터": "https://cdn.pixabay.com/photo/2016/01/13/07/22/hamster-1136909_1280.jpg",
    "기니피그": "https://cdn.pixabay.com/photo/2016/09/07/11/37/cavia-1658329_1280.jpg",
    "앵무새": "https://cdn.pixabay.com/photo/2016/02/19/10/00/macaw-1208271_1280.jpg",
    "코브라": "https://cdn.pixabay.com/photo/2019/11/09/18/53/cobra-4612713_1280.jpg"
}

fallback_image = "https://cdn.pixabay.com/photo/2016/11/21/16/01/cat-1845789_1280.jpg"

image_url = pet_images.get(best_pet, fallback_image)

st.image(image_url, caption=f"{best_pet} 사진", use_column_width=True)
