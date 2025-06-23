from fastapi import APIRouter
from src.schemas.summary_schema import SummaryRequest, SummaryResponse
from src.services.summary_service import summarize_chat

router = APIRouter()

# 대화 요약 생성 엔드포인트
@router.post(
    "/summary",
    response_model=SummaryResponse
)
async def summary_endpoint(body: SummaryRequest):
    return await summarize_chat(body)