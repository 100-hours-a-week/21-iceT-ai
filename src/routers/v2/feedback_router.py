from fastapi import APIRouter

from src.schemas.feedback_schema import (
    FeedbackRequest, FeedbackResponse,
    FeedbackAnswerRequest, FeedbackAnswerResponse
)
from src.services.feedback_service import explain_feedback, answer_feedback_question

router = APIRouter()

# 1. 피드백 시작 (코드 리뷰)
@router.post("/feedback", response_model=FeedbackResponse)
async def feedback_start(req: FeedbackRequest):
    result = await explain_feedback(req)
    return FeedbackResponse(
        sessionId=req.sessionId,  # ✅ 요청에서 받은 sessionId 사용
        problemNumber=req.problemNumber,
        title=result.title,
        good=result.good,
        bad=result.bad,
        improvedCode=result.improvedCode
    )



# 2. 자유 응답 (챗봇)
@router.post("/feedback/answer", response_model=FeedbackAnswerResponse)
async def feedback_answer(req: FeedbackAnswerRequest):
    return await answer_feedback_question(req)