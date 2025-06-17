# src/services/feedback_service.py

from src.adapters.llm_chat import generate
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

async def answer_feedback_question(req: FeedbackAnswerRequest) -> FeedbackAnswerResponse:
    if not any(m.role == "user" for m in req.messages):
        raise ValueError("대화에 사용자 메시지가 최소 1개는 포함되어야 합니다.")

    prompt = build_prompt_from_memory(req.messages, req.summary, recent_turns=5, mode="feedback")

    # 💬 역할 강조 + 반복 방지 + JSON 지시
    system_prompt = (
        "너는 사용자의 코드에 대해 대화를 이어가는 **친절하지만 똑똑한 코드 리뷰어**야.\n"
        "- 사용자의 이전 질문을 반복해서 답하지 마.\n"
        "- 필요하면 코드블럭으로 예시 코드를 제공해.\n"
        "- 사용자가 무엇을 물었는지 명확히 파악하고, 그 의도에 맞게 구체적인 정보를 줘.\n"
        "- 항상 JSON 형식으로 `{ \"answer\": \"...\" }` 만 응답해."
    )

    # 🧠 요약 삽입
    if req.summary:
        system_prompt += f"\n\n📝 이전 대화 요약: {req.summary.strip()}"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]

    if settings.use_upstage:
        return await generate(messages, schema_class=FeedbackAnswerResponse)
    else:
        raw_output = await generate(messages)
        parsed = json.loads(raw_output.strip().strip("```json").strip("```"))
        return FeedbackAnswerResponse(sessionId=req.sessionId, answer=parsed["answer"])
