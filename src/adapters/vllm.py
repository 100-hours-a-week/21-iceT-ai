from langchain_community.chat_models import ChatOpenAI
from src.config import settings
from dotenv import load_dotenv

load_dotenv()

# LangChain ChatOpenAI 인터페이스를 vLLM 서버에 연결
llm = ChatOpenAI(
    openai_api_key="EMPTY",  # 로컬 vLLM 서버에서는 키 무시
    openai_api_base="http://localhost:8001/v1",
    model_name=settings.model,
    temperature=settings.temperature,
    max_tokens=settings.max_tokens,
    top_p=0.9,
    # ✅ 정지 토큰 설정 (안정성 향상)
    stop=["</s>"]
)

# ✅ 메시지 또는 문자열 프롬프트 모두 지원
def generate(messages_or_prompt) -> str:
    if isinstance(messages_or_prompt, str):
        return llm.invoke(messages_or_prompt)
    elif isinstance(messages_or_prompt, list):
        return llm.invoke(messages_or_prompt)
    else:
        raise ValueError("generate()는 str 또는 ChatML 메시지 리스트만 지원합니다.")