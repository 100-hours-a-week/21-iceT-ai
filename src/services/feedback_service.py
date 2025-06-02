# src/services/feedback_service.py

from adapters.llm_chat import generate
from src.schemas.feedback_schema import (
    FeedbackRequest, FeedbackResponse,
    FeedbackAnswerRequest, FeedbackAnswerResponse
)
from src.core.prompt_templates import format_feedback_prompt
from src.core.prompt_builders import build_prompt_from_memory
from src.config import settings
import json

# 1. /feedback/start: 코드 피드백 생성
async def explain_feedback(req: FeedbackRequest) -> FeedbackResponse:
    data = req.model_dump()
    prompt = format_feedback_prompt(data)

    messages = [
        {"role": "system", "content": "You are a professional code reviewer. Always respond in correct JSON."},
        {"role": "user", "content": prompt}
    ]

    if settings.use_upstage:
        return await generate(messages, schema_class=FeedbackResponse)
    else:
        raw_output = await generate(messages, schema_class=None)
        parsed = json.loads(raw_output.strip().strip("```json").strip("```"))
        return FeedbackResponse(
            sessionId=req.sessionId,
            problemNumber=req.problemNumber,
            title=req.title,
            good=parsed["good"],
            bad=parsed["bad"],
            improvedCode=parsed["improved_code"]
        )

# 2. /feedback/answer: 자유 질문 응답
async def answer_feedback_question(req: FeedbackAnswerRequest) -> FeedbackAnswerResponse:
    if not any(m.role == "user" for m in req.messages):
        raise ValueError("대화에 사용자 메시지가 최소 1개는 포함되어야 합니다.")

    prompt = build_prompt_from_memory(req.messages, req.summary, recent_turns=3, mode="feedback")
    messages = [
        {"role": "system", "content": "You are a helpful and kind code review assistant. Respond clearly and concisely."},
        {"role": "user", "content": prompt}
    ]

    if settings.use_upstage:
        return await generate(messages, schema_class=FeedbackAnswerResponse)
    else:
        raw_output = await generate(messages)
        parsed = json.loads(raw_output.strip().strip("```json").strip("```"))
        return FeedbackAnswerResponse(sessionId=req.sessionId, answer=parsed["answer"])
