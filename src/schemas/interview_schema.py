from pydantic import BaseModel, Field
from typing import List

class InterviewStartRequest(BaseModel):
    problemNumber: int = Field(description="문제 번호")
    title: str = Field(description="문제 제목")
    description: str = Field(description="문제 설명")
    inputRule: str = Field(description="입력 조건 설명")
    outputRule: str = Field(description="출력 조건 설명")
    intputExample: str = Field(description="입력 예시")
    outputExample: str = Field(description="출력 예시")
    codeLanguage: str = Field(description="프로그래밍 언어 (예: python, cpp, java)")
    code: str = Field(description="사용자 제출 코드")

class InterviewStartResponse(BaseModel):
    problemNumber: int = Field(description="문제 번호")
    title: str = Field(description="문제 제목")
    question: str = Field(description="AI가 생성한 첫 면접 질문")

class Message(BaseModel):
    role: str = Field(description='"user" 또는 "assistant" 역할')
    content: str = Field(description="메시지 내용")

class InterviewAnswerRequest(BaseModel):
    sessionId: str = Field(description="면접 세션 ID")
    messages: List[Message] = Field(description="이전 대화 이력")

class InterviewAnswerResponse(BaseModel):
    sessionId: str = Field(description="면접 세션 ID")
    question: str = Field(description="AI가 생성한 꼬리 질문")

class InterviewEndRequest(BaseModel):
    sessionId: str = Field(description="면접 세션 ID")
    messages: List[Message] = Field(description="면접 전체 대화 기록")

class InterviewReview(BaseModel):
    good: List[str] = Field(description="잘한 점")
    bad: List[str] = Field(description="부족했던 점")
    improvement: List[str] = Field(description="개선 사항 제안")

class InterviewEndResponse(BaseModel):
    review: InterviewReview = Field(description="AI가 생성한 구조화된 면접 총평")
