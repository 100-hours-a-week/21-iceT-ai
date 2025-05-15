import logging, asyncio
from langchain_openai import ChatOpenAI
from src.config import settings
from dotenv import load_dotenv
from src.schemas.solution_schema import SolutionResponse

# 환경변수 로드
load_dotenv()

# 로깅
logger = logging.getLogger(__name__)

# Langchain LLM 클라이언트 설정
llm = ChatOpenAI(
    model=settings.model,
    temperature=settings.temperature,
    max_tokens=settings.max_tokens,
)

# LLM의 응답을 Pydantic 모델로 구조화하기 위한 래퍼
structured_llm = llm.with_structured_output(SolutionResponse)

# 프롬프트 모델에 전달하고 구조화된 응답 반환
async def generate_solution(prompt: str) -> SolutionResponse:
    try:
        # OpenAI 비동기 호출
        return await asyncio.wait_for(structured_llm.ainvoke(prompt), timeout=60)
    except Exception as e:
        logger.error("LLM 호출 실패", exc_info=True)
        raise RuntimeError("해설 생성 중 오류가 발생했습니다.") from e
    

# async def generate_solution(prompt: str) -> SolutionResponse:
#     response = await structured_llm.ainvoke(prompt)
#     return response