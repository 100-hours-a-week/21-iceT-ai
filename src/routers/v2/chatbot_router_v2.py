from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from langsmith import traceable

from src.schemas.chatbot_schema import (
    InterviewStartRequest, InterviewfollowRequest,
    FeedbackRequest, FeedbackfollowRequest,
    SummaryRequest, SummaryResponse
)
from src.services.chatbot_service_v2 import ChatbotService

router = APIRouter()
service = ChatbotService()

# --- Interview ---
@router.post("/interview/start")
@traceable(run_type="tool", name="POST_interview_start", tags=["api", "interview", "start"])
async def interview_start(req: InterviewStartRequest):
    """면접 시작 - 첫 번째 질문 생성"""
    stream = service.start_interview(req)
    return StreamingResponse(stream, media_type="text/event-stream")

@router.post("/interview/answer")
@traceable(run_type="tool", name="POST_interview_answer", tags=["api", "interview", "answer"])
async def interview_answer(req: InterviewfollowRequest):
    """면접 진행 - 후속 질문 또는 평가 생성"""
    stream = service.followup_interview(req)
    return StreamingResponse(stream, media_type="text/event-stream")

# --- Feedback ---
@router.post("/feedback/start")
@traceable(run_type="tool", name="POST_feedback_start", tags=["api", "feedback", "start"])
async def feedback_start(req: FeedbackRequest):
    """피드백 시작 - 잘한 점, 개선할 점, 개선된 코드 생성"""
    stream = service.start_feedback(req)
    return StreamingResponse(stream, media_type="text/event-stream")

@router.post("/feedback/answer")
@traceable(run_type="tool", name="POST_feedback_answer", tags=["api", "feedback", "answer"])
async def feedback_answer(req: FeedbackfollowRequest):
    """피드백 후속 질문 대응"""
    stream = service.followup_feedback(req)
    return StreamingResponse(stream, media_type="text/event-stream")

# --- Summary ---
@router.post("/summary", response_model=SummaryResponse)
@traceable(run_type="tool", name="POST_summary", tags=["api", "summary"])
async def summary_endpoint(req: SummaryRequest):
    """대화 요약 생성"""
    return await service.summarize(req)
