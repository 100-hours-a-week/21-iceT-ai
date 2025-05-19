from langchain_community.llms import VLLMOpenAI
from src.config import settings
from dotenv import load_dotenv

load_dotenv()

# LangChain vLLM 클라이언트
llm = VLLMOpenAI(
    openai_api_key="EMPTY",  # vLLM 서버는 키를 검증하지 않음
    openai_api_base="http://localhost:8001/v1",
    model_name=settings.model,
    model_kwargs={
        "temperature": settings.temperature,
        "max_tokens": settings.max_tokens,
        "top_p": 0.9,
    },
)

# 메시지 목록 or 프롬프트 텍스트를 받아 응답 문자열을 반환
def generate(prompt_or_messages):
    return llm.invoke(prompt_or_messages)
