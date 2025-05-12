from langchain_community.llms import VLLMOpenAI
from src.config import settings
from dotenv import load_dotenv

load_dotenv()

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

# 구조화 없이 텍스트만 반환
def generate(prompt: str) -> str:
    return llm.invoke(prompt)
