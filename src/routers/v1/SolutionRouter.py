from fastapi import APIRouter, HTTPException
from models.SolutionSchema import SolutionRequest, SolutionResponse
from services.SolutionService import explainSolution

router = APIRouter()

@router.post("/solution", response_model=SolutionResponse)
async def solutionEndpoint(body: SolutionRequest):
    try:
        return await explainSolution(body)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
