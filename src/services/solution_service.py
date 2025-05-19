# src/services/solution_service.py

from src.adapters.vllm import generate
from src.schemas.solution_schema import SolutionRequest, SolutionResponse
from src.core.llm_utils import parse_solution_response
from src.core.prompt_templates import format_solution_prompt  # ✅ 리팩토링된 포맷 함수 사용

# 문제 해설 생성 함수
async def explain_solution(req: SolutionRequest) -> SolutionResponse:
    # 1. 프롬프트 문자열 직접 생성
    prompt = format_solution_prompt({
        "problem_number": req.problem_number,
        "title": req.title,
        "description": req.description,
        "input": req.input,
        "output": req.output,
        "input_example": req.input_example,
        "output_example": req.output_example,
    })

    # 2. ChatML 메시지 구성
    messages = [
        {"role": "system", "content": "You are a helpful assistant that explains algorithm problems in JSON format only."},
        {"role": "user", "content": prompt}
    ]

    # 3. LLM 호출 (vLLM)
    raw_output = await generate(messages)

    # 4. JSON 파싱
    return parse_solution_response(raw_output)
