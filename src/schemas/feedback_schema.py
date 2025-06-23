from pydantic import BaseModel, Field
from typing import List, Optional

class Message(BaseModel):
    role: str = Field(description='"user" 또는 "assistant"')
    content: str = Field(description="메시지 내용")

class FeedbackRequest(BaseModel):
    sessionId: str = Field(description="세션 ID")
    problemNumber: int = Field(description="문제 번호")
    title: str = Field(description="문제 제목")
    description: str = Field(description="문제 설명")
    inputRule: str = Field(description="입력 조건 설명")
    outputRule: str = Field(description="출력 조건 설명")
    inputExample: str = Field(description="입력 예시")
    outputExample: str = Field(description="출력 예시")
    codeLanguage: str = Field(description="프로그래밍 언어 (예: python, cpp, java)")
    code: str = Field(description="사용자 제출 코드")

class FeedbackfollowRequest(BaseModel):
    sessionId: str = Field(description="챗 세션 ID")
    messages: List[Message] = Field(description="대화 메시지 리스트")
    summary: Optional[str] = Field(default=None, description="이전 요약 (선택사항)")
    staticSummary: Optional[str] = Field(default=None, description="문제 정보 요약 (고정, 선택사항)")