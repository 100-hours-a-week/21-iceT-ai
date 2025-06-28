import logging, re
from src.core.prompt_templates import SOLUTION_PROMPT
from src.adapters.llm_solution import generate_solution
from src.schemas.solution_schema import SolutionRequest, SolutionResponse
from src.core.vector_store import load_vectorstore

logger = logging.getLogger(__name__)

retriever = load_vectorstore().as_retriever()

# 문제 요청을 기반으로 해설 생성하는 서비스 함수
async def explain_solution(req: SolutionRequest) -> SolutionResponse:
    docs = await retriever.ainvoke(req.description)
    context = "\n\n".join(d.page_content[:500] for d in docs)

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
    
    result = await generate_solution(prompt)
    return result