from pydantic import BaseModel
from typing import List

class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class FeedbackChatRequest(BaseModel):
    session_id: str
    messages: List[Message]

class FeedbackChatResponse(BaseModel):
    session_id: str
    answer: str
