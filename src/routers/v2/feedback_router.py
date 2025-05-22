from fastapi import APIRouter
from uuid import uuid4

from src.schemas.feedback_schema import (
    FeedbackRequest, FeedbackResponse,
    FeedbackAnswerRequest, FeedbackAnswerResponse
)
from src.services.feedback_service import explain_feedback, answer_feedback_question

router = APIRouter()

# 1. 피드백 시작 (코드 리뷰)
@router.post("/feedback", response_model=FeedbackResponse)
async def feedback_start(req: FeedbackRequest):
    session_id = str(uuid4())
    result = await explain_feedback(req)
    return FeedbackResponse(
        sessionId=session_id,
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