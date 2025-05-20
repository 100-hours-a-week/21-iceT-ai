# src/services/feedback_service.py

from src.adapters.vllm import generate
from src.schemas.feedback_schema import (
    FeedbackRequest, FeedbackResponse,
    FeedbackAnswerRequest, FeedbackAnswerResponse
)
from src.core.prompt_templates import format_feedback_prompt
from src.core.llm_utils import parse_feedback_response

# 1. /feedback: 코드 피드백 생성
async def explain_feedback(req: FeedbackRequest) -> FeedbackResponse:
    try:
        data = req.model_dump()
    except Exception as e:
        print("❌ model_dump 실패:", e)
        raise

    try:
        prompt = format_feedback_prompt(data)
    except Exception as e:
        print("❌ 프롬프트 포맷 실패:", e)
        raise

    messages = [
        {"role": "system", "content": "You are a professional code reviewer. Always respond in correct JSON."},
        {"role": "user", "content": prompt}
    ]

    raw_output = await generate(messages)
    return parse_feedback_response(raw_output, title=data.get("title", "제목 없음"))


# 2. /feedback/answer: 챗봇 자유 응답
async def answer_feedback_question(req: FeedbackAnswerRequest) -> FeedbackAnswerResponse:
    messages = [{"role": m.role, "content": m.content} for m in req.messages]

    if not messages or messages[-1]["role"] != "user":
        raise ValueError("마지막 메시지는 반드시 사용자여야 합니다.")

    messages.insert(0, {
        "role": "system",
        "content": "You are a helpful and kind code review assistant. Respond clearly and concisely."
    })

    output = await generate(messages)
    return FeedbackAnswerResponse(session_id=req.session_id, answer=output.strip())
