from fastapi import APIRouter

from src.schemas.feedback_schema import (
    FeedbackRequest, FeedbackResponse,
    FeedbackAnswerRequest, FeedbackAnswerResponse
)
from src.services.feedback_service import explain_feedback, answer_feedback_question

from sse_starlette.sse import EventSourceResponse
from src.adapters.llm_chat import stream_generate
from src.core.prompt_builders import build_prompt_from_memory
from src.schemas.feedback_schema import FeedbackAnswerRequest

router = APIRouter()

@router.post("/feedback/start-stream")
async def feedback_start_stream(req: FeedbackRequest):
    from src.core.prompt_templates import format_feedback_prompt

    # 1. 프롬프트 구성
    prompt = format_feedback_prompt(req.model_dump())

    messages = [
        {"role": "system", "content": "너는 친절하고 명확한 코드 리뷰어야. stream 방식으로 차례대로 설명해줘."},
        {"role": "user", "content": prompt}
    ]

    # 2. 스트리밍 생성기
    async def event_generator():
        async for token in stream_generate(messages):
            yield {"event": "message", "data": token}

    return EventSourceResponse(event_generator())

@router.post("/feedback/answer-stream")
async def feedback_answer_stream(req: FeedbackAnswerRequest):
    # 1. 사용자 메시지 확인
    if not any(m.role == "user" for m in req.messages):
        raise ValueError("대화에 사용자 메시지가 최소 1개는 포함되어야 합니다.")

    # 2. 요약 정규화
    summary_data = req.summary
    if isinstance(summary_data, str):
        try:
            import json
            summary_data = json.loads(summary_data)
        except:
            summary_data = [{"speaker": "ai", "content": summary_data}]

    # 3. 프롬프트 생성
    prompt = build_prompt_from_memory(req.messages, summary_data, recent_turns=5, mode="feedback")

    # 4. system prompt 구성
    system_prompt = (
        "너는 사용자의 코드에 대해 대화를 이어가는 **친절하지만 똑똑한 코드 리뷰어**야.\n"
        "- 이전 대화 요약을 참고해서 대화를 자연스럽게 이어가.\n"
        "- 사용자가 무엇을 물었는지 명확히 파악하고, 그 의도에 맞게 구체적인 정보를 줘.\n"
        "- JSON 응답은 필요 없어. 그냥 자연스럽게 stream 방식으로 말해줘."
    )

    # 5. 메시지 조립
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]

    # 6. 토큰 스트리밍
    async def event_generator():
        async for token in stream_generate(messages):
            yield {"event": "message", "data": token}

    return EventSourceResponse(event_generator())

# 1. 피드백 시작 (코드 리뷰)
@router.post("/feedback/start", response_model=FeedbackResponse)
async def feedback_start(req: FeedbackRequest):
    result = await explain_feedback(req)
    return FeedbackResponse(
        sessionId=req.sessionId,
        problemNumber=req.problemNumber,
        title=result.title,
        good=result.good,
        bad=result.bad,
        improvedCode=result.improvedCode
    )

# 2. 자유 응답 (챗봇)
@router.post("/feedback/answer", response_model=FeedbackAnswerResponse)
async def feedback_answer(req: FeedbackAnswerRequest):
    return await answer_feedback_question(req)