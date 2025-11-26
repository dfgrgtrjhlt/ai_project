import streamlit as st
import pandas as pd
import altair as alt
from io import StringIO

st.set_page_config(page_title="경기도 시군별 반려동물 현황", layout="wide")

# -------------------------------
# 🎉 초기 효과
# -------------------------------
st.balloons()

# -------------------------------
# 📘 CSV 파일 불러오기
# -------------------------------
st.title("🐾 경기도 시군별 반려동물 등록 현황")
st.write("CSV 시각화 + 반려동물 추천 + 동물 사진 표시를 포함한 종합 분석 앱입니다.")

uploaded_file = st.file_uploader("CSV 파일을 업로드하세요 (UTF-8 또는 CP949 인코딩 지원)", type=["csv"])
df = None

def read_csv_safely(file):
    """Try cp949 → utf-8 automatically."""
    for enc in ["cp949", "utf-8"]:
        try:
            return pd.read_csv(file, encoding=enc)
        except:
            file.seek(0)
            continue
    raise Exception("CSV 파일 인코딩을 읽을 수 없습니다.")

if uploaded_file:
    df = read_csv_safely(uploaded_file)
else:
    default_path = "/mnt/data/dkdrlahWL.csv"
    try:
        with open(default_path, "rb") as f:
            df = read_csv_safely(f)
            st.info("기본 CSV 파일(/mnt/data/dkdrlahWL.csv)을 불러왔습니다.")
    except:
        st.warning("CSV 파일을 업로드하거나 기본 경로에 파일을 준비해주세요.")
        st.stop()

# -------------------------------
# 데이터 전처리
# -------------------------------
df.columns = [c.strip() for c in df.columns]
required = ["시군명", "등록동물수(마리)", "동물소유자수", "동물품종수"]

for col in required:
    if col not in df.columns:
        st.error(f"❌ CSV에 '{col}' 컬럼이 없습니다.")
        st.stop()

for col in ["등록동물수(마리)", "동물소유자수", "동물품종수"]:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace(",", "")
        .str.replace(" ", "")
        .replace({"": "0", "nan": "0"})
    )
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

grouped = df.groupby("시군명", as_index=False).sum()

# -------------------------------
# 🎨 무지개 색상 지정
# -------------------------------
rainbow = ["#ff0000", "#ff7f00", "#ffff00", "#00ff00", "#0000ff", "#8b00ff"]
grouped = grouped.sort_values("등록동물수(마리)", ascending=False)
grouped["color"] = (rainbow * ((len(grouped) // len(rainbow)) + 1))[: len(grouped)]

# -------------------------------
# 🌈 무지개 막대그래프
# -------------------------------
st.subheader("🌈 시군별 등록 동물 수 (무지개 색상)")

bar = (
    alt.Chart(grouped)
    .mark_bar()
    .encode(
        x=alt.X("시군명:N", sort="-y"),
        y="등록동물수(마리):Q",
        color=alt.Color("color:N", scale=None, legend=None),
        tooltip=["시군명", "등록동물수(마리)", "동물소유자수"]
    )
)
st.altair_chart(bar, use_container_width=True)

st.markdown("---")



# -------------------------------
# 🐶🐱 반려동물 추천 시스템 + 사진
# -------------------------------
st.header("💡 반려동물 추천받기")

q1 = st.radio("1️⃣ 집 평수는 어떤가요?", ["좁음", "보통", "넓음"])
q2 = st.radio("2️⃣ 활동량을 얼마나 원하나요?", ["적음", "보통", "많음"])
q3 = st.radio("3️⃣ 털 관리가 귀찮나요?", ["예", "아니오"])
q4 = st.radio("4️⃣ 조용한 동물이 좋나요?", ["예", "아니오"])

pet_images = {
    "강아지": "https://images.unsplash.com/photo-1518717758536-85ae29035b6d",
    "고양이": "https://images.unsplash.com/photo-1518791841217-8f162f1e1131",
    "햄스터": "https://images.unsplash.com/photo-1589578527966-fdac0f44566a",
    "기니피그": "https://images.unsplash.com/photo-1610389058530-4313d1cc4036",
    "앵무새": "https://images.unsplash.com/photo-1501705789558-40c785c33f61",
    "코브라": "https://images.unsplash.com/photo-1610986606365-71bcc25f9945"
}

if st.button("반려동물 추천 받기 💖"):
    scores = {p: 0 for p in pet_images.keys()}

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

    best_score = max(scores.values())
    best_pet = [p for p, s in scores.items() if s == best_score][0]

    st.subheader(f"✨ 당신에게 어울리는 반려동물은 **{best_pet}** 입니다!")
    st.image(pet_images[best_pet], width=350)
    st.snow()
    st.success("💖 소중한 반려동물을 사랑해주세요! 💖")

st.markdown("---")

st.write("더 많은 한국어 전용 AI는 https://gptonline.ai/ko/ 에서 확인하세요 😊")
