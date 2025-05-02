from fastapi import APIRouter
from src.schemas.solution_schema import SolutionRequest, SolutionResponse
from src.services.solution_service import explain_solution

router = APIRouter()

# 백준 문제 해설 생성 엔드포인트
# - 요청 본문: SolutionRequest 스키마 (문제 정보 포함)
# - 응답: SolutionResponse 스키마 (해설, 정답 코드 포함)

# POST /api/v1/solution
@router.post("/solution", response_model=SolutionResponse)
async def solution_endpoint(body: SolutionRequest):
    return await explain_solution(body)
