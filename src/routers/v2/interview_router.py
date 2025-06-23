from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from src.schemas.interview_schema import InterviewStartRequest, InterviewfollowRequest, InterviewEndRequest
from src.services.interview_service import (
    handle_interview_start,
    handle_interview_answer,
    handle_interview_end
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

@router.post("/interview/end")
async def interview_end(req: InterviewEndRequest):
    stream = await handle_interview_end(req)
    return StreamingResponse(stream, media_type="text/event-stream")