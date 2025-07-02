# GPT 해설 생성 호출

from src.solchat.services.v2.solution_service_v2 import explain_solution
from src.solchat.schemas.v2.solution_schema_v2 import SolutionRequest, SolutionResponse

async def generate_explanation(request: SolutionRequest) -> SolutionResponse:
    return await explain_solution(request)