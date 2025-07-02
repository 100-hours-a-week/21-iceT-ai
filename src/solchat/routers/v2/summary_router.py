from typing import List
from fastapi import APIRouter
from src.solchat.schemas.v2.summary_schema import SummaryRequest, SummaryResponse
from src.solchat.services.v2.summary_service import summarize_chat

router = APIRouter()

# 대화 요약 생성 엔드포인트
@router.post("/summary", response_model=List[SummaryResponse])
async def summary_endpoint(bodies: List[SummaryRequest]):
    return await summarize_chat(bodies)