import asyncio
import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from src.config import settings
from src.schemas.solution_schema import SolutionResponse

# Gemini LLM 클라이언트 설정 (항상 사용)
llm = ChatGoogleGenerativeAI(
    model=settings.gemini_model,
    temperature=settings.sol_temperature,
    max_tokens=settings.sol_max_tokens,
    google_api_key=settings.gemini_api_key
)

# LLM의 응답을 Pydantic 모델로 구조화하기 위한 래퍼
structured_llm = llm.with_structured_output(SolutionResponse)

# 프롬프트 모델에 전달하고 구조화된 응답 반환
async def generate_solution(prompt: str) -> SolutionResponse:
    try:
        return await asyncio.wait_for(structured_llm.ainvoke(prompt), timeout=300)
    except Exception as e:
        raise RuntimeError("해설 생성 중 오류가 발생했습니다.") from e

"""
async def generate_solution(prompt: str) -> str:
    try:
        return await llm.ainvoke(prompt)  # 구조화 없이 호출
    except Exception as e:
        logging.error(f"해설 생성 중 오류 발생: {e}")
        raise RuntimeError("해설 생성 중 오류가 발생했습니다.") from e
"""