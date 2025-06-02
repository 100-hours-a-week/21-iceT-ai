# src/services/solution_service.py

from src.adapters.llm_main import generate
from src.schemas.solution_schema import SolutionRequest, SolutionResponse
from src.core.llm_utils import parse_solution_response
from src.core.prompt_templates import format_solution_prompt
from src.config import settings

# 문제 해설 생성 함수
async def explain_solution(req: SolutionRequest) -> SolutionResponse:
    # 1. 프롬프트 문자열 직접 생성
    prompt = format_solution_prompt({
        "problemNumber": req.problemNumber,
        "title": req.title,
        "description": req.description,
        "input": req.input,
        "output": req.output,
        "inputExample": req.inputExample,
        "outputExample": req.outputExample,
    })


    # 2. ChatML 메시지 구성
    messages = [
        {"role": "system", "content": "You are a helpful assistant that explains algorithm problems in JSON format only."},
        {"role": "user", "content": prompt}
    ]

# 3. Upstage/vLLM 분기 처리
    if settings.use_upstage:
        # Upstage: structured output 사용
        return await generate(messages, schema_class=SolutionResponse)
    else:
        # vLLM: 기존 방식
        raw_output = await generate(messages)
        print("✅ [DEBUG] LLM 응답:\n", raw_output)
        return parse_solution_response(raw_output)
