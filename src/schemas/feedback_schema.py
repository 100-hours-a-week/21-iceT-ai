from pydantic import BaseModel, Field
from typing import List, Optional

class FeedbackRequest(BaseModel):
    problemNumber: int = Field(description="문제 번호")
    title: str = Field(description="문제 제목")
    description: str = Field(description="문제 설명")
    inputRule: str = Field(description="입력 조건 설명")
    outputRule: str = Field(description="출력 조건 설명")
    intputExample: str = Field(description="입력 예시")
    outputExample: str = Field(description="출력 예시")
    codeLanguage: str = Field(description="프로그래밍 언어 (예: python, cpp, java)")
    code: str = Field(description="사용자 제출 코드")

class FeedbackResponse(BaseModel):
    sessionId: str = Field(description="챗 세션 ID")
    problemNumber: int = Field(description="문제 번호")
    title: str = Field(description="문제 제목")
    good: List[str] = Field(description="코드에서 잘한 점")
    bad: List[str] = Field(description="코드에서 개선할 점")
    improvedCode: str = Field(description="AI가 제안한 개선된 코드")

class Message(BaseModel):
    role: str = Field(description='"user" 또는 "assistant"')
    content: str = Field(description="메시지 내용")

class FeedbackAnswerRequest(BaseModel):
    sessionId: str
    messages: List[Message]
    summary: Optional[str] = Field(default=None, description="이전 요약 (선택사항)")

class FeedbackAnswerResponse(BaseModel):
    sessionId: str = Field(description="챗 세션 ID")
    answer: str = Field(description="AI 응답 메시지")

