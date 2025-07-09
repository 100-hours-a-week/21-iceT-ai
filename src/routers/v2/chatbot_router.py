from typing import List
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from src.schemas.chatbot_schema import (
    InterviewStartRequest, InterviewfollowRequest,
    FeedbackRequest, FeedbackfollowRequest,
    SummaryRequest, SummaryResponse
)
from src.services.chatbot_service import (
    handle_interview_start, handle_interview_answer,
    handle_feedback_start, handle_feedback_answer,
    summarize_chat
)

router = APIRouter()

# --- Interview ---
@router.post("/interview/start")
async def interview_start(req: InterviewStartRequest):
    stream = await handle_interview_start(req)
    return StreamingResponse(stream, media_type="text/event-stream")

@router.post("/interview/answer")
async def interview_answer(req: InterviewfollowRequest):
    stream = await handle_interview_answer(req)
    return StreamingResponse(stream, media_type="text/event-stream")

# --- Feedback ---
@router.post("/feedback/start")
async def feedback_start(req: FeedbackRequest):
    stream = await handle_feedback_start(req)
    return StreamingResponse(stream, media_type="text/event-stream")

@router.post("/feedback/answer")
async def feedback_answer(req: FeedbackfollowRequest):
    stream = await handle_feedback_answer(req)
    return StreamingResponse(stream, media_type="text/event-stream")

# --- Summary ---
@router.post("/summary", response_model=List[SummaryResponse])
async def summary_endpoint(bodies: List[SummaryRequest]):
    return await summarize_chat(bodies)