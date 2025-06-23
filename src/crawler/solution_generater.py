from src.services.solution_service import explain_solution
from src.schemas.solution_schema import SolutionRequest, SolutionResponse

# 문제 요청을 기반으로 해설을 생성하는 비동기 함수
async def generate_explanation(request: SolutionRequest) -> SolutionResponse:
    return await explain_solution(request)