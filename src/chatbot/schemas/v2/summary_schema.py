from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class Message(BaseModel):
    role: str
    content: str

class Summary(BaseModel):
    type: Literal["problem", "chat"] = Field(default="chat", description='"problem" 또는 "chat"')
    speaker: str = Field(description='"user", "ai", 또는 "system"')
    intent: str = Field(description="발화 의도 (예: 질문, 설명, 반박, 분석 등)")
    content: str = Field(description="요약된 발화 내용")

class SummaryRequest(BaseModel):
    sessionId: int = Field(description="세션 ID")
    messages: List[Message] = Field(description="요약할 메시지 목록 (user/assistant role 포함)")

class SummaryResponse(BaseModel):
    sessionId: int = Field(description="세션 ID")
    summary: str = Field(description="문제 정보와 대화 요약을 담은 긴 텍스트")