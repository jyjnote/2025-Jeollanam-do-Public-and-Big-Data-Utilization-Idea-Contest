import streamlit as st
import requests

# ✅ Falcon-7B-Instruct 텍스트 생성용 API
API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
headers = {
    "Authorization": "Bearer ",
    "Content-Type": "application/json"
}

# ✅ Falcon-7B는 chat 형식이 아니라 text generation이므로 prompt만 사용
def query(prompt):
    try:
        payload = {
            "inputs": prompt,
            "parameters": {
                "temperature": 0.7,
                "max_new_tokens": 512
            }
        }

        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()

        result = response.json()
        # ✅ Falcon 응답은 {'generated_text': "..."} 형태의 리스트임
        if isinstance(result, list):
            return result[0].get("generated_text", "⚠️ 결과 없음")
        else:
            return result.get("generated_text", "⚠️ 결과 없음")

    except requests.exceptions.RequestException as e:
        return f"요청 실패: {e}"
    except requests.exceptions.JSONDecodeError:
        return f"⚠️ JSON 디코딩 실패:\n{response.text}"

def render():
    st.subheader("📄 정책 리포트 생성")
    topic = st.text_input("분석 주제 입력", placeholder="예: 고령화 대응 방안")

    if topic:
        with st.spinner("🧠 GPT 리포트 생성 중..."):
            responder = GPTResponder()
            report = responder.ask(f"{topic}에 대한 전라남도 맞춤형 정책 제안 리포트 작성해줘.")
            st.markdown(report)
