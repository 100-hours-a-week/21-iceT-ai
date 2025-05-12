import json
from src.core.prompt_templates import SOLUTION_PROMPT
from src.adapters.llm_selector import llm
from src.schemas.solution_schema import SolutionRequest, SolutionResponse

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

    # 2. ✅ ChatML 구조로 메시지 생성
    messages = [
        {"role": "system", "content": "You are a helpful assistant that explains algorithm problems in JSON format only."},
        {"role": "user", "content": prompt}
    ]

    # 3. 모델 응답 받기 (Qwen via vLLM, messages 포맷으로)
    raw_output = llm.invoke(messages)

    # 4. JSON 파싱 및 예외 처리
    try:
        parsed = json.loads(raw_output)
        return SolutionResponse(**parsed)
    except Exception as e:
        raise ValueError(
            f"❌ Qwen 응답을 JSON으로 파싱하지 못했습니다.\n\n[원본 응답]:\n{raw_output}\n\n[에러]: {e}"
        )