import logging, anyio
from src.core.prompt_templates import SOLUTION_PROMPT
from src.adapters.llm_client import generate_solution
from src.schemas.solution_schema import SolutionRequest, SolutionResponse
from src.core.vector_store import load_vectorstore

# 로깅
logger = logging.getLogger(__name__)

# FAISS에서 검색 가능하도록 retriever 생성
retriever = load_vectorstore().as_retriever()

# 문제 요청을 기반으로 해설 생성하는 서비스 함수
async def explain_solution(req: SolutionRequest) -> SolutionResponse:
    # 문제 설명 기반으로 관련 문서 검색
    docs = await retriever.ainvoke(req.description)
    context = "\n\n".join(d.page_content[:500] for d in docs)  # 길이 제한

    # 프롬프트 템플릿에 문제 정보 삽입
    prompt = SOLUTION_PROMPT.invoke(
        {
            "problem_number": req.problem_number,
            "title":          req.title,
            "description":    req.description,
            "input":          req.input,
            "output":         req.output,
            "input_example":  req.input_example,
            "output_example": req.output_example,
            "context":        context
        }
    )

    # LLM에 프롬프트 전송하여 해설 생성
    result = await generate_solution(prompt)
    return result