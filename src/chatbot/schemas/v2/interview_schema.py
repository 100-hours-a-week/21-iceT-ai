from pydantic import BaseModel, Field
from typing import List, Optional

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
    summary: Optional[str] = None