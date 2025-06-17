from typing import List
from pydantic import BaseModel, Field

class ChatMessage(BaseModel):
    role: str
    content: str

class SummaryRequest(BaseModel):
    sessionId: str = Field(description="세션 ID")
    messages: List[ChatMessage] = Field(description="요약할 메시지 목록 (user/assistant role 포함)")
    maxSentences: int = Field(default=3, description="요약 결과 최대 문장 수")
    mode: str = Field(description="요약 모드 (feedback 또는 interview)")

class SummaryResponse(BaseModel):
    sessionId: str = Field(description="세션 ID")
    summary: str = Field(description="요약 결과")