from typing import List, Optional, Union
from pydantic import BaseModel, Field

class ChatMessage(BaseModel):
    role: str
    content: str

class TurnSummary(BaseModel):
    speaker: str = Field(description='"user" 또는 "ai"')
    intent: str = Field(description="발화 의도 (예: 질문, 설명, 반박, 분석 등)")
    content: str = Field(description="요약된 발화 내용")

class SummaryRequest(BaseModel):
    sessionId: str = Field(description="세션 ID")
    messages: List[ChatMessage] = Field(description="요약할 메시지 목록 (user/assistant role 포함)")
    maxSentences: int = Field(default=3, description="요약 결과 최대 문장 수")
    mode: str = Field(description="요약 모드 (feedback 또는 interview)")
    staticSummary: Optional[Union[str, List[dict]]] = Field(
        default=None,
        description="변하지 않는 문제 정보 요약 (선택)"
    )

class TurnSummaryResponse(BaseModel):
    sessionId: str = Field(description="세션 ID")
    summary: List[TurnSummary] = Field(description="대화 요약 리스트")
    staticSummary: Optional[Union[str, List[dict]]] = Field(
        default=None,
        description="(선택) 고정된 문제 요약 내용"
    )
