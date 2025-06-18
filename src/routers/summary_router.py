from fastapi import APIRouter
from src.schemas.summary_schema import SummaryRequest, TurnSummaryResponse
from src.services.summary_service import generate_summary

router = APIRouter()

@router.post("/summary", response_model=TurnSummaryResponse)
async def summary(req: SummaryRequest):
    return await generate_summary(req)