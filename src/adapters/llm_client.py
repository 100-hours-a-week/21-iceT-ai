from langchain_openai import ChatOpenAI
from config import settings
from dotenv import load_dotenv
from models.solution_schema import SolutionResponse

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
    """
    LangChain LLM 클라이언트를 사용하여 솔루션 생성
    """
    response = structured_llm.invoke(prompt)
    return response
