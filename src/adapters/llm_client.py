from langchain_openai import ChatOpenAI
from src.config import settings
from dotenv import load_dotenv
from src.schemas.solution_schema import SolutionResponse

# 환경변수 로드
load_dotenv()

# Langchain LLM 클라이언트 설정
llm = ChatOpenAI(
    model=settings.model,
    temperature=settings.temperature,
    max_tokens=settings.max_tokens,
)

structured_llm = llm.with_structured_output(SolutionResponse)

def generate_solution(prompt: str) -> SolutionResponse:
    response = structured_llm.invoke(prompt)
    return response
