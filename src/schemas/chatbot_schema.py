from pydantic import BaseModel, Field
from typing import List, Optional, Literal

# 공통 메시지 모델
class Message(BaseModel):
    role: str = Field(description='"user", "assistant", 또는 "system" 역할')
    content: str = Field(description="메시지 내용")

# --- Interview ---
class InterviewStartRequest(BaseModel):
    sessionId: int
    problemNumber: int
    title: str
    description: str
    inputDescription: str
    outputDescription: str
    inputExample: str
    outputExample: str
    codeLanguage: str
    code: str

class InterviewfollowRequest(BaseModel):
    sessionId: int
    messages: List[Message]
    summary: Optional[str] = None

# --- Feedback ---
class FeedbackRequest(BaseModel):
    sessionId: int = Field(description="세션 ID")
    problemNumber: int = Field(description="문제 번호")
    title: str = Field(description="문제 제목")
    description: str = Field(description="문제 설명")
    inputDescription: str = Field(description="입력 조건 설명")
    outputDescription: str = Field(description="출력 조건 설명")
    inputExample: str = Field(description="입력 예시")
    outputExample: str = Field(description="출력 예시")
    codeLanguage: str = Field(description="프로그래밍 언어 (예: python, cpp, java)")
    code: str = Field(description="사용자 제출 코드")

class FeedbackfollowRequest(BaseModel):
    sessionId: int = Field(description="챗 세션 ID")
    messages: List[Message] = Field(description="대화 메시지 리스트")
    summary: Optional[str] = Field(default=None, description="이전 요약 (선택사항)")

# --- Summary ---
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