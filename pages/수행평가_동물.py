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
# 💖 커스텀 하트 이펙트
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

# -------------------------------------------------
# 📄 CSV 읽기
# -------------------------------------------------
df = pd.read_csv("dkdrlahWL.csv", encoding="cp949")
grouped = df.groupby("시군명")["등록동물수(마리)"].sum().reset_index()

# -------------------------------------------------
# 🌈 무지개 색상
# ---------------------------------
