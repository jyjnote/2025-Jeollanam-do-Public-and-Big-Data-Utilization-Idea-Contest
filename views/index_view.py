import streamlit as st

def render():
    st.subheader("📍 정주지수 보기")
    selected_region = st.selectbox("지역 선택", ["전체", "순천", "여수", "목포", "광양"])
    # 실제 데이터 로직은 이후에 추가
    st.metric("정주지수", "78", delta="+3")
    st.progress(0.78)
    st.info(f"{selected_region}의 정주지수는 상대적으로 양호한 편입니다.")
