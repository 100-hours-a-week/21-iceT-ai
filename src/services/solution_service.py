from src.adapters.llm_solution import generate_solution
from src.schemas.solution_schema import SolutionRequest, SolutionResponse
from src.core.prompt_templates import SOLUTION_PROMPT
from src.core.vector_store import load_vectorstore
from src.config import settings
import json

retriever = load_vectorstore().as_retriever()

async def explain_solution(req: SolutionRequest) -> SolutionResponse:
    # 문제 설명 기반으로 관련 문서 검색
    docs = await retriever.ainvoke(req.description)
    context = "\n\n".join(d.page_content[:500] for d in docs)  # 길이 제한

    # 프롬프트 템플릿에 문제 정보 삽입
    prompt = SOLUTION_PROMPT.invoke(
        {
            "problemNumber":  req.problemNumber,
            "title":          req.title,
            "description":    req.description,
            "input":          req.input,
            "output":         req.output,
            "inputExample":   req.inputExample,
            "outputExample":  req.outputExample,
            "context":        context
        }
    )

    # LLM에 프롬프트 전송하여 해설 생성
    result = await generate_solution(prompt)
    return result