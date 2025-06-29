# GPT 해설 생성 호출

from services.v1.solution_service import explain_solution
from schemas.v1.solution_schema import SolutionRequest, SolutionResponse

async def generate_explanation(request: SolutionRequest) -> SolutionResponse:
    return await explain_solution(request)