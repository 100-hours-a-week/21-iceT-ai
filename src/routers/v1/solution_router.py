from fastapi import APIRouter, Depends, Header, HTTPException, status
from src.schemas.solution_schema import SolutionRequest, SolutionResponse
from src.services.solution_service import explain_solution

router = APIRouter()

# 백준 문제 해설 생성 엔드포인트
@router.post(
    "/solution",
    response_model=SolutionResponse
)
async def solution_endpoint(body: SolutionRequest):
    return await explain_solution(body)
