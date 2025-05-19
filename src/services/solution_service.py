from src.core.prompt_templates import SOLUTION_PROMPT
from src.adapters.vllm import llm
from src.schemas.solution_schema import SolutionRequest, SolutionResponse
from src.core.llm_utils import parse_solution_response  # ✅ 추가

async def explain_solution(req: SolutionRequest) -> SolutionResponse:
    # 1. 기존 방식으로 프롬프트 텍스트 생성
    prompt = SOLUTION_PROMPT.invoke({
        "problem_number": req.problem_number,
        "title": req.title,
        "description": req.description,
        "input": req.input,
        "output": req.output,
        "input_example": req.input_example,
        "output_example": req.output_example
    })

    # 2. ChatML 메시지 구성
    messages = [
        {"role": "system", "content": "You are a helpful assistant that explains algorithm problems in JSON format only."},
        {"role": "user", "content": prompt}
    ]

    # 3. 모델 응답 받기 (vLLM)
    raw_output = llm.invoke(messages)

    # 4. JSON 파싱 → 유틸 함수로
    return parse_solution_response(raw_output)
