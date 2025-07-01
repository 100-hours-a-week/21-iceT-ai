from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from src.schemas.v2.interview_schema import InterviewStartRequest, InterviewfollowRequest
from src.services.v2.interview_service import (
    handle_interview_start,
    handle_interview_answer
)

router = APIRouter()

@router.post("/interview/start")
async def interview_start(req: InterviewStartRequest):
    stream = await handle_interview_start(req)
    return StreamingResponse(stream, media_type="text/event-stream")

@router.post("/interview/answer")
async def interview_answer(req: InterviewfollowRequest):
    stream = await handle_interview_answer(req)
    return StreamingResponse(stream, media_type="text/event-stream")