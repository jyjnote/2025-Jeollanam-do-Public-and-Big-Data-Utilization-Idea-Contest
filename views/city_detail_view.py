import streamlit as st

def render():
    st.subheader("🏙️ 도시별 상세보기")
    city = st.selectbox("도시 선택", ["목포", "순천", "여수", "광양", "해남"])
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("💼 노동시장 분석")
        st.bar_chart({"제조업": 40, "서비스업": 30, "기타": 30})
    with col2:
        st.write("🚑 의료/교통 인프라")
        st.metric("병원 수", 12)
        st.metric("평균 통근 시간", "18분")
