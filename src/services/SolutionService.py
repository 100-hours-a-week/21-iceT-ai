import json
from adapters.LlmClient import generateSolution
from models.SolutionSchema import SolutionRequest, SolutionResponse
from core.PromptTemplates import getSolutionPrompt


async def explainSolution(req: SolutionRequest) -> SolutionResponse:
    prompt = getSolutionPrompt(
        req.problem_number,
        req.title,
        req.description,
        req.input_example,
        req.output_example,
        req.language,
    )
    content = generateSolution(prompt)
    # 모델이 반환한 JSON 텍스트 파싱
    data = json.loads(content)
    return SolutionResponse(**data)
