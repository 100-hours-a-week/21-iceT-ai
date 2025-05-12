from src.config import settings
from dotenv import load_dotenv

load_dotenv()

if settings.llm_provider != "openai":
    raise ImportError("llm_client_base.py는 LLM_PROVIDER=openai일 때만 로드되어야 합니다.")

from langchain_openai import ChatOpenAI
from src.schemas.solution_schema import SolutionResponse

llm = ChatOpenAI(
    model=settings.model,
    temperature=settings.temperature,
    max_tokens=settings.max_tokens,
)

structured_llm = llm.with_structured_output(SolutionResponse)

async def generate_solution(prompt: str) -> SolutionResponse:
    return await structured_llm.ainvoke(prompt)
