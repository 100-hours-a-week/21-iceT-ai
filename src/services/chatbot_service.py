import httpx
import asyncio
import logging
from typing import List, AsyncGenerator

from src.config import settings, BACKEND_INTERVIEW_URL
from src.adapters.llm_client_v2 import (
    call_interview_agent,
    call_feedback_agent,
    generate_summary,
)
from src.schemas.chatbot_schema import (
    InterviewStartRequest, InterviewfollowRequest,
    FeedbackRequest, FeedbackfollowRequest,
    SummaryRequest, SummaryResponse
)
from src.core.prompt_templates_v2 import (
    INTERVIEW_START_PROMPT, INTERVIEW_FLOW_DECIDER_PROMPT, QUESTION_AGENT_PROMPT,
    FOLLOWUP_AGENT_PROMPT, EVALUATION_AGENT_PROMPT,
    FEEDBACK_START_PROMPT, FEEDBACK_ANSWER_PROMPT
)
from src.core.chat_history import build_context_text

logger = logging.getLogger(__name__)

# 인터뷰 서비스

async def notify_interview_end(session_id: int):
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(
                BACKEND_INTERVIEW_URL,
                json={"sessionId": session_id, "isFinished": True},
            )
            if response.status_code != 200:
                logger.warning(f"[notify_interview_end] 상태코드 {response.status_code}: {response.text}")
    except Exception as e:
        logger.warning(f"[notify_interview_end] 호출 실패: {e}")

async def handle_interview_start(req: InterviewStartRequest):
    problem_text = f"{req.title}\n{req.description}\n입력: {req.inputDescription}\n출력: {req.outputDescription}\n예시: {req.inputExample} → {req.outputExample}"
    prompt = INTERVIEW_START_PROMPT.format(problem=problem_text, language=req.codeLanguage)
    return await call_interview_agent(
        prompt,
        stream=True,
        max_tokens=settings.max_tokens_interview_start,
        session_id=req.sessionId, 
    )

async def handle_interview_answer(req: InterviewfollowRequest) -> AsyncGenerator[str, None]:
    messages = [{"role": m.role, "content": m.content} for m in req.messages]
    context_text = build_context_text(messages, summary=getattr(req, "summary", None))

    # 대화 흐름 판단 (followup / question / end)
    flow_decision = await call_interview_agent(
        INTERVIEW_FLOW_DECIDER_PROMPT.format(context=context_text),
        stream=False,
        max_tokens=10
    )
    decision = flow_decision.strip().lower()

    # 종료 판단 → 총평 스트리밍
    if decision == "end":
        evaluation_stream = await call_interview_agent(
            EVALUATION_AGENT_PROMPT.format(context=context_text),
            stream=True,
            max_tokens=settings.max_tokens_interview_end,
            session_id=req.sessionId,
        )
        asyncio.create_task(notify_interview_end(req.sessionId))
        return evaluation_stream

    # followup or question → 스트리밍 질문 생성
    if decision == "followup":
        previous_question = messages[-2]["content"] if len(messages) >= 2 and messages[-2]["role"] == "assistant" else ""
        user_response = messages[-1]["content"] if len(messages) >= 1 and messages[-1]["role"] == "user" else ""

        followup_stream = await call_interview_agent(
            FOLLOWUP_AGENT_PROMPT.format(
                previous_question=previous_question,
                user_response=user_response
            ),
            stream=True,
            max_tokens=settings.max_tokens_interview_start,
            session_id=req.sessionId,
        )
        return followup_stream

    else:  # "question" 또는 fallback
        avoid_list = "\n".join(f"- {m['content']}" for m in messages if m["role"] == "assistant")

        question_stream = await call_interview_agent(
            QUESTION_AGENT_PROMPT.format(
                context=context_text,
                avoid_list=avoid_list
            ),
            stream=True,
            max_tokens=settings.max_tokens_interview_start,
            session_id=req.sessionId,
        )
        return question_stream

# 피드백 서비스

async def handle_feedback_start(req: FeedbackRequest):
    prompt = FEEDBACK_START_PROMPT.format(
        problem=req.description,
        code=req.code,
        language=req.codeLanguage,
    )
    return await call_feedback_agent(
        prompt,
        stream=True,
        max_tokens=settings.max_tokens_feedback_start
    )

async def handle_feedback_answer(req: FeedbackfollowRequest):
    messages = [{"role": m.role, "content": m.content} for m in req.messages]
    context_text = build_context_text(messages, summary=getattr(req, "summary", None))
    prompt = FEEDBACK_ANSWER_PROMPT.format(
        context=context_text,
        user_input=req.messages[-1].content
    )
    return await call_feedback_agent(
        prompt,
        stream=True,
        max_tokens=settings.max_tokens_feedback_answer,
        session_id=req.sessionId,
    )

# 요약 서비스

async def summarize_chat(requests: List[SummaryRequest]) -> List[SummaryResponse]:
    tasks = [generate_summary(r) for r in requests]
    return await asyncio.gather(*tasks)