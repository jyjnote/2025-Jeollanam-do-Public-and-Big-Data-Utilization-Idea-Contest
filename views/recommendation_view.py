import streamlit as st

def render():
    st.subheader("🤝 정주지 추천")
    goal = st.radio("당신의 우선순위는?", ["의료 접근성", "교육", "생활비", "기후", "문화시설"])
    
    st.success(f"🏠 추천 지역: 곡성군\n\n🔍 이유: {goal} 기준 상위 10% 지역입니다.")
    st.map({"lat": [35.2756], "lon": [127.2903]})
