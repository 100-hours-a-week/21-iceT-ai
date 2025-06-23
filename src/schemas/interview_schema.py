from pydantic import BaseModel, Field
from typing import List

class Message(BaseModel):
    role: str = Field(description='"user" 또는 "assistant" 역할')
    content: str = Field(description="메시지 내용")

class InterviewStartRequest(BaseModel):
    sessionId: str
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
    sessionId: str
    messages: List[Message]
    summary: str  # JSON string. 문제+대화 요약 모두 포함 ("type": "problem" / "chat")

class InterviewEndRequest(BaseModel):
    sessionId: str
    messages: List[Message]
    summary: str  # 위와 동일하게 통합
