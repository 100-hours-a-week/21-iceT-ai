from fastapi import APIRouter
from src.schemas.chat_schema import FeedbackChatRequest, FeedbackChatResponse
from src.services.feedback_chat_service import handle_feedback_chat

router = APIRouter()

@router.post("/feedback/chat", response_model=FeedbackChatResponse)
async def feedback_chat(req: FeedbackChatRequest):
    return await handle_feedback_chat(req)
