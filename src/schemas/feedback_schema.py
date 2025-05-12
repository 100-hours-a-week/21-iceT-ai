from pydantic import BaseModel
from typing import List

class FeedbackRequest(BaseModel):
    title: str  # 원래 있던 필드 (모델이 생성하게 할 수도 있음)
    description: str
    input_rule: str
    output_rule: str
    sample_input: str
    sample_output: str
    code_language: str
    code: str

class FeedbackResponse(BaseModel):
    title: str
    good: List[str]
    bad: List[str]
    improved_code: str

class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class FeedbackAnswerRequest(BaseModel):
    session_id: str
    messages: List[Message]

class FeedbackAnswerResponse(BaseModel):
    session_id: str
    answer: str
