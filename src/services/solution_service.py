import json
from src.core.prompt_templates import SOLUTION_PROMPT
from src.adapters.llm_selector import llm
from src.schemas.solution_schema import SolutionRequest, SolutionResponse

async def explain_solution(req: SolutionRequest) -> SolutionResponse:
    # 1. 프롬프트 생성
    prompt = SOLUTION_PROMPT.invoke({
        "problem_number": req.problem_number,
        "title": req.title,
        "description": req.description,
        "input": req.input,
        "output": req.output,
        "input_example": req.input_example,
        "output_example": req.output_example
    })

    # 2. 모델 응답 받기 (Qwen)
    raw_output = llm.invoke(prompt)

    # 3. JSON 파싱
    try:
        parsed = json.loads(raw_output)
        return SolutionResponse(**parsed)
    except Exception as e:
        raise ValueError(f"❌ Qwen 응답을 JSON으로 파싱하지 못했습니다.\n\n[원본 응답]:\n{raw_output}\n\n[에러]: {e}")
