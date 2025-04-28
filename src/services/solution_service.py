import json
from adapters.llm_client import generate_solution
from models.solution_schema import SolutionRequest, SolutionResponse
from core.prompt_templates import get_solution_prompt


async def explain_solution(req: SolutionRequest) -> SolutionResponse:
    prompt = get_solution_prompt(
        req.problem_number,
        req.title,
        req.description,
        req.input_example,
        req.output_example,
        req.language,
    )
    content = generate_solution(prompt)
    # 모델이 반환한 JSON 텍스트 파싱
    data = json.loads(content)
    return SolutionResponse(**data)
