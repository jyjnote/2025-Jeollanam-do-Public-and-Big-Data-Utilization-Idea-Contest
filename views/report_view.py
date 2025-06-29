import streamlit as st
from gpt_engine.langchain_interface import GPTResponder

def render():
    st.subheader("📄 정책 리포트 생성")
    topic = st.text_input("분석 주제 입력", placeholder="예: 고령화 대응 방안")

    if topic:
        with st.spinner("🧠 GPT 리포트 생성 중..."):
            responder = GPTResponder()
            report = responder.ask(f"{topic}에 대한 전라남도 맞춤형 정책 제안 리포트 작성해줘.")
            st.markdown(report)
