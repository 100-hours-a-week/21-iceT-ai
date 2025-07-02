from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from src.chatbot.schemas.v2.feedback_schema import FeedbackRequest, FeedbackfollowRequest
from src.chatbot.services.v2.feedback_service import handle_feedback_start, handle_feedback_answer

router = APIRouter()

@router.post("/feedback/start")
async def feedback_start(req: FeedbackRequest):
    stream = await handle_feedback_start(req)
    return StreamingResponse(stream, media_type="text/event-stream")

@router.post("/feedback/answer")
async def feedback_answer(req: FeedbackfollowRequest):
    stream = await handle_feedback_answer(req)
    return StreamingResponse(stream, media_type="text/event-stream")
