from fastapi import APIRouter
from src.schemas.feedback_schema import FeedbackRequest, FeedbackResponse, FeedbackAnswerRequest, FeedbackAnswerResponse
from src.services.feedback_service import explain_feedback, answer_feedback_question

router = APIRouter()

# 1. 코드 피드백 생성
@router.post("/feedback", response_model=FeedbackResponse)
async def feedback_start(req: FeedbackRequest):
    return await explain_feedback(req)

# 2. 자유 응답 (챗봇)
@router.post("/feedback/answer", response_model=FeedbackAnswerResponse)
async def feedback_answer(req: FeedbackAnswerRequest):
    return await answer_feedback_question(req)