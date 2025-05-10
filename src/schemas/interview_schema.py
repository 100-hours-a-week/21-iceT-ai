from pydantic import BaseModel
from typing import List

class InterviewStartRequest(BaseModel):
    title: str
    number: int
    description: str
    input_rule: str
    output_rule: str
    sample_input: str
    sample_output: str
    code: str
    code_language: str

class InterviewStartResponse(BaseModel):
    title: str
    question: str

class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class InterviewAnswerRequest(BaseModel):
    session_id: str
    messages: List[Message]

class InterviewAnswerResponse(BaseModel):
    session_id: str
    question: str

class InterviewEndRequest(BaseModel):
    messages: List[Message]
    session_id: str

class InterviewEndResponse(BaseModel):
    review: str
