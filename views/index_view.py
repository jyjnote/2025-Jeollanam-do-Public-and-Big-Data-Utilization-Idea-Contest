import streamlit as st

def render():
    st.subheader("📍 정주지수 대시보드")

    # 선택 가능한 지역
    selected_region = st.selectbox("지역 선택", ["전체", "순천", "여수", "목포", "광양"])

    # 예시 데이터 (임의값, 추후 실제 데이터와 연동 가능)
    data = {
        "순천": {"total": 82, "교육": 80, "복지": 85, "주거": 77, "문화": 80, "교통": 88, "일자리": 75, "안전": 85},
        "여수": {"total": 75, "교육": 72, "복지": 70, "주거": 74, "문화": 78, "교통": 70, "일자리": 72, "안전": 80},
        "목포": {"total": 68, "교육": 65, "복지": 60, "주거": 70, "문화": 66, "교통": 62, "일자리": 64, "안전": 72},
        "광양": {"total": 73, "교육": 70, "복지": 75, "주거": 69, "문화": 71, "교통": 74, "일자리": 70, "안전": 76},
        "전체": {"total": 74, "교육": 72, "복지": 72, "주거": 72, "문화": 74, "교통": 73, "일자리": 70, "안전": 76},
    }

    region_data = data[selected_region]

    st.metric("✅ 종합 정주지수", f"{region_data['total']}", delta="+3")
    st.progress(region_data['total'] / 100)

    # 지표 별 시각화
    with st.expander("세부 지표 보기"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🎓 교육", region_data["교육"])
            st.metric("🏥 복지", region_data["복지"])
        with col2:
            st.metric("🏠 주거", region_data["주거"])
            st.metric("🎭 문화", region_data["문화"])
        with col3:
            st.metric("🚌 교통", region_data["교통"])
            st.metric("💼 일자리", region_data["일자리"])
            st.metric("🛡️ 안전", region_data["안전"])

    st.info(f"ℹ️ {selected_region}의 정주지수는 주요 생활환경 지표를 기반으로 종합 평가된 값입니다.")
