from fastapi import APIRouter
from src.schemas.chat_schema import SummaryRequest, SummaryResponse
from src.services.summary_service import generate_summary

router = APIRouter()

@router.post("/summary", response_model=SummaryResponse)
async def summary(req: SummaryRequest):
    return await generate_summary(req)
