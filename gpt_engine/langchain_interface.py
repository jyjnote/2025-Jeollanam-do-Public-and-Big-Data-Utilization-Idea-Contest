from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

class GPTResponder:
    def __init__(self, model_name="gpt-4"):
        # 환경변수 OPENAI_API_KEY를 LangChain이 자동으로 사용
        self.chat = ChatOpenAI(model_name=model_name, temperature=0.7)

    def ask(self, prompt: str) -> str:
        try:
            messages = [HumanMessage(content=prompt)]
            response = self.chat(messages)
            return response.content.strip()
        except Exception as e:
            return f"❌ 오류 발생: {str(e)}"
