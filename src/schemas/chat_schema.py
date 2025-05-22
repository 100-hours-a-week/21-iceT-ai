from pydantic import BaseModel, Field
from typing import List

class Message(BaseModel):
    role: str = Field(description='"user" 또는 "assistant" 역할')
    content: str = Field(description="메시지 내용")

class FeedbackChatRequest(BaseModel):
    sessionId: str = Field(description="챗 세션 ID")
    messages: List[Message] = Field(description="대화 메시지 목록")

class FeedbackChatResponse(BaseModel):
    sessionId: str = Field(description="챗 세션 ID")
    answer: str = Field(description="AI 응답 메시지")
