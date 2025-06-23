import logging, asyncio
from langchain_google_genai import ChatGoogleGenerativeAI
from src.config import settings
from dotenv import load_dotenv
from src.schemas.solution_schema import SolutionResponse
import os

load_dotenv()

logger = logging.getLogger(__name__)

llm = ChatGoogleGenerativeAI(
    model=settings.model_solution,
    temperature=settings.temperature_solution,
    max_tokens=settings.max_tokens_solution,
    google_api_key=os.getenv("GEMINI_API_KEY")
)

structured_llm = llm.with_structured_output(SolutionResponse)

async def generate_solution(prompt: str) -> SolutionResponse:
    try:
        return await asyncio.wait_for(structured_llm.ainvoke(prompt), timeout=300)
    except Exception as e:
        logger.error("LLM 호출 실패", exc_info=True)
        raise RuntimeError("해설 생성 중 오류가 발생했습니다.") from e
