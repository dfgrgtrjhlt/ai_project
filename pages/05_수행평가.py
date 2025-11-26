import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# --- 1. 설정 및 데이터 로드 ---
st.set_page_config(
    page_title="반려동물 등록 현황 및 추천",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data

def load_data():
    # 현재 파일(page.py)의 상위폴더 = 프로젝트 루트
    base_path = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(base_path, 'data', 'pet_data.csv')

    try:
        df = pd.read_csv(data_path, encoding='cp949')

        
        # 컬럼 이름 정리 (불필요한 공백 제거)
        df.columns = df.columns.str.strip()
        
        # '등록동물수(마리)'를 숫자로 변환 (결측치는 0으로 처리)
        df['등록동물수(마리)'] = pd.to_numeric(df['등록동물수(마리)'], errors='coerce').fillna(0).astype(int)
        
        # 2025년 데이터 필터링 (분석 결과에서 2025년 데이터가 가장 풍부했음)
        df_2025 = df[df['기준년도'] == 2025]
        
        # 시군별 등록동물수 합산
        region_data = df_2025.groupby('시군명')['등록동물수(마리)'].sum().sort_values(ascending=False)
        
        return region_data

    except FileNotFoundError:
        st.error(f"⚠️ 데이터 파일 ({data_path})을 찾을 수 없습니다. 'data' 폴더에 'pet_data.csv'를 올바르게 배치했는지 확인하세요.")
        return None
    except Exception as e:
        st.error(f"⚠️ 데이터 로드 중 오류 발생: {e}")
        return None


# --- 2. 반려동물 등록 현황 시각화 ---
def visualize_data(region_data):
    """시군별 등록 현황을 막대 그래프로 표시합니다."""
    st.header("경기도 시군별 반려동물 등록 현황 (2025년 기준)")
    st.caption("제공된 데이터를 기준으로 시군별 등록된 동물의 수를 합산한 결과입니다.")
    
    if region_data is not None and not region_data.empty:
        # Matplotlib을 사용하여 한글 폰트 설정
        plt.rcParams['font.family'] = 'Malgun Gothic' # Windows 기준. Linux/Mac 환경에서는 'AppleGothic' 등으로 변경 필요
        plt.rcParams['axes.unicode_minus'] = False # 마이너스 폰트 깨짐 방지
        
        fig, ax = plt.subplots(figsize=(12, 6))
        region_data.plot(kind='bar', ax=ax, color='skyblue')
        
        ax.set_title('시군별 등록동물수 (2025)', fontsize=16)
        ax.set_xlabel('시군명', fontsize=12)
        ax.set_ylabel('등록동물수 (마리)', fontsize=12)
        plt.xticks(rotation=45, ha='right') # x축 레이블 회전
        plt.tight_layout()
        
        st.pyplot(fig)
    elif region_data is not None:
        st.warning("2025년 등록 데이터가 없습니다.")


# --- 3. 설문 기반 반려동물 추천 시스템 ---
def pet_recommendation():
    """간단한 설문을 통해 반려동물을 추천합니다."""
    
    st.header("나에게 맞는 반려동물 추천 설문")
    st.caption("간단한 4가지 질문으로 당신에게 어울리는 반려동물을 찾아보세요.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        q1 = st.radio(
            "1. 활동적인 편인가요? 반려동물과 함께 **산책이나 운동**을 즐기고 싶습니다.",
            ('예', '아니오'),
            key='q1'
        )
        
        q2 = st.radio(
            "2. **털 관리에 품**을 들이는 것이 어렵지 않나요? (잦은 빗질, 목욕 등)",
            ('예', '아니오'),
            key='q2'
        )

    with col2:
        q3 = st.radio(
            "3. **잦은 소음**이나 울음소리에 크게 신경 쓰지 않는 편입니다.",
            ('예', '아니오'),
            key='q3'
        )

        q4 = st.radio(
            "4. **혼자 있는 시간**이 많아도 괜찮은, 독립적인 반려동물을 원합니다.",
            ('예', '아니오'),
            key='q4'
        )

    st.markdown("---")
    
    if st.button("나의 반려동물 추천 받기"):
        # 추천 로직
        if q1 == '예' and q3 == '예':
            recommendation = "강아지"
            description = "강아지는 활동적이며 주인과 교감하는 것을 좋아합니다. 규칙적인 산책과 활동을 함께 할 수 있는 분께 적합합니다."
            image_url = "https://images.unsplash.com/photo-1597633214736-22485c2921a2?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        elif q1 == '아니오' and q4 == '아니오':
            recommendation = "고양이"
            description = "고양이는 강아지보다 독립적이지만, 주인과의 조용한 교감을 즐깁니다. 적당한 관심과 청결한 환경을 제공할 수 있는 분께 좋습니다."
            image_url = "https://images.unsplash.com/photo-1574158622682-e40e6988c187?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        elif q2 == '아니오': # 털 관리가 어렵지 않다는 답변
            recommendation = "도마뱀"
            description = "도마뱀은 털 관리가 전혀 필요 없고, 소음이 거의 없으며, 사육 환경만 잘 갖춰준다면 비교적 독립적인 사육이 가능합니다. 이색적인 반려동물을 원하시는 분께 추천합니다."
            image_url = "https://images.unsplash.com/photo-1558229868-b715a31e3d06?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        elif q4 == '예':
            recommendation = "햄스터"
            description = "햄스터는 작은 공간에서 키울 수 있으며, 비교적 독립적이어서 혼자 있는 시간이 많은 분께 부담이 적습니다. 활동량이 적은 반려동물을 원하시는 분께 추천합니다."
            image_url = "https://images.unsplash.com/photo-1597813083416-2911299e5250?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        else:
            recommendation = "강아지 또는 고양이"
            description = "답변만으로는 명확한 구분이 어렵습니다. 활동량과 독립성 등 개인의 생활 패턴을 고려하여 강아지나 고양이 중 선택해보세요."
            image_url = "https://images.unsplash.com/photo-1560706248-267923485d56?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" # 강아지/고양이 함께 있는 이미지

        
        st.subheader(f"✨ 당신에게 추천하는 반려동물은 바로... **{recommendation}**입니다!")
        st.info(description)
        
        # 추천 동물 이미지 표시 (웹 URL 사용)
        st.image(image_url, caption=f"추천 동물: {recommendation}", use_column_width=True)

# --- 메인 함수 실행 ---
def main():
    st.title("🐾 반려동물 등록 현황 분석 및 나만의 펫 추천 서비스")
    
    # 1. 데이터 시각화 섹션
    region_data = load_data()
    visualize_data(region_data)
    
    st.markdown("---")
    
    # 2. 추천 설문 섹션
    pet_recommendation()

if __name__ == "__main__":
    main()
