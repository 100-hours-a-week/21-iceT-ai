from fastapi import APIRouter
from src.models.solution_schema import SolutionRequest, SolutionResponse
from src.services.solution_service import explain_solution

router = APIRouter()

# POST /api/v1/solution
@router.post("/solution", response_model=SolutionResponse)
async def solution_endpoint(body: SolutionRequest):
    return await explain_solution(body)
