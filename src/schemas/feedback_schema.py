from pydantic import BaseModel
from typing import List

class FeedbackRequest(BaseModel):
    title: str
    description: str
    code: str

class FeedbackResponse(BaseModel):
    title: str
    good: List[str]
    bad: List[str]
    improved_code: str

class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class FeedbackAnswerRequest(BaseModel):
    session_id: str
    messages: List[Message]

class FeedbackAnswerResponse(BaseModel):
    session_id: str
    answer: str
