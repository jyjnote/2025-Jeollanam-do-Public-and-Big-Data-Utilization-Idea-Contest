import streamlit as st

def render():
    st.subheader("🧪 정책 시뮬레이션")
    budget = st.slider("예산 배분 (억 원)", 0, 1000, 200)
    sector = st.multiselect("투자 분야", ["의료", "교육", "교통", "주거", "산업 육성"])

    st.write(f"💰 배분한 예산: {budget}억 원")
    st.write(f"📊 선택된 분야: {', '.join(sector)}")

    if st.button("시뮬레이션 실행"):
        st.success("🚀 시뮬레이션 결과: 예상 정주지수 +5 상승, 고용률 +2% 증가")
