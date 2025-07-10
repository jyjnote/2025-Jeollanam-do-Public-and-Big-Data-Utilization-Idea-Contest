import streamlit as st
import pandas as pd
import altair as alt
import random

def generate_random_value(base, variance):
    return round(base + random.uniform(-variance, variance), 1)

def render():
    st.subheader("💼 지역 노동시장 대시보드")

    # 지역 선택
    regions = ["전체", "순천", "여수", "목포", "광양", "해남"]
    selected_region = st.selectbox("📍 지역 선택", regions)

    # 무작위 값 생성
    total_employed = f"{generate_random_value(75000, 10000):,.0f}명"
    avg_work_hours = f"{generate_random_value(40, 3)}시간"
    wage_per_hour = f"₩{generate_random_value(17000, 2000):,.0f}"
    total_wage = f"₩{generate_random_value(1300, 150):,.0f}억"

    # KPI 카드
    col0, col1, col2, col3 = st.columns(4)
    with col0:
        st.metric("총 고용 인원", total_employed, "+5.1% YoY")
    with col1:
        st.metric("평균 노동 시간", avg_work_hours, "-0.4시간")
    with col2:
        st.metric("노동 단가", wage_per_hour, "+2.8%")
    with col3:
        st.metric("총 임금 지출", total_wage, "+4.3%")

    st.divider()

    # 산업별 고용 비중 + 직무별 평균 노동시간
    col4, col5 = st.columns([2, 3])
    with col4:
        st.markdown("### 🧭 산업별 고용 비중")
        job_data = pd.DataFrame({
            "산업": ["제조업", "서비스업", "농림어업", "건설업", "IT/기타"],
            "비율": [random.randint(10, 35) for _ in range(5)]
        })
        chart = alt.Chart(job_data).mark_arc(innerRadius=50).encode(
            theta="비율",
            color="산업",
            tooltip=["산업", "비율"]
        )
        st.altair_chart(chart, use_container_width=True)

    with col5:
        st.markdown("### ⏱️ 직무별 평균 노동시간")
        hour_data = pd.DataFrame({
            "직무": ["기계", "전기", "사무/행정", "영업/유통", "기타"],
            "시간": [generate_random_value(36, 5) for _ in range(5)]
        })
        st.bar_chart(hour_data.set_index("직무"))

    st.divider()

    # 고용 유형별 상태
    st.markdown("### 📊 고용 유형별 상태 (작업 진척도 포함)")

    col6, col7, col8 = st.columns(3)
    with col6:
        st.metric("정규직", f"{random.randint(40000, 60000):,}명")
        st.progress(random.uniform(0.7, 0.9), "근무 만족도")
    with col7:
        st.metric("비정규직", f"{random.randint(10000, 20000):,}명")
        st.progress(random.uniform(0.4, 0.6), "근속 기간")
    with col8:
        st.metric("일용직", f"{random.randint(8000, 15000):,}명")
        st.progress(random.uniform(0.3, 0.5), "업무 안정도")

    st.divider()

    # 분야별 인력 수요 및 임금
    st.markdown("### 📋 분야별 인력 수요 및 임금")
    table_data = pd.DataFrame({
        "분야": ["기계", "전기", "사무", "운전", "건설"],
        "수요인원": [random.randint(1000, 5000) for _ in range(5)],
        "평균임금(만원)": [random.randint(250, 420) for _ in range(5)],
        "최근 1년 변화율": [f"{random.choice(['+', '-'])}{round(random.uniform(0.5, 5.0), 1)}%" for _ in range(5)]
    })
    st.dataframe(table_data, use_container_width=True)
