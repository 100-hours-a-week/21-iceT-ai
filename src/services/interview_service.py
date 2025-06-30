import httpx
import asyncio
from typing import AsyncGenerator
from src.config import settings, BACKEND_INTERVIEW_URL  # ✅ BACKEND_INTERVIEW_URL 추가
from src.core.utils.history_utils import build_context_text
from src.adapters.llm_interview import call_agent
from src.schemas.interview_schema import InterviewStartRequest, InterviewfollowRequest  # ✅ InterviewEndRequest 제거
from src.core.prompt_templates import INTERVIEW_START_PROMPT, QUESTION_AGENT_PROMPT, FOLLOWUP_AGENT_PROMPT, FINISH_DECISION_PROMPT, EVALUATION_AGENT_PROMPT
from src.core.utils.stream_utils import wrap_static_response, wrap_stream_response
import logging

logger = logging.getLogger(__name__)

# ✅ 백엔드 인터뷰 종료 알림 비동기 POST 함수 (2-2)
async def notify_interview_end(session_id: str):
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(
                BACKEND_INTERVIEW_URL,
                json={"sessionId": session_id, "isFinished": True},
            )
            if response.status_code != 200:
                logging.warning(f"[notify_interview_end] 상태코드 {response.status_code}: {response.text}")
    except Exception as e:
        logging.warning(f"[notify_interview_end] 호출 실패: {e}")

# ✅ /interview/start
async def handle_interview_start(req: InterviewStartRequest):
    problem_text = f"{req.title}\n{req.description}\n입력: {req.inputRule}\n출력: {req.outputRule}\n예시: {req.inputExample} → {req.outputExample}"
    prompt = INTERVIEW_START_PROMPT.format(problem=problem_text, language=req.codeLanguage)
    return await call_agent(
        prompt,
        stream=True,
        max_tokens=settings.max_tokens_interview_start 
    )

async def handle_interview_answer(req: InterviewfollowRequest) -> AsyncGenerator[str, None]:
    messages = [{"role": m.role, "content": m.content} for m in req.messages]
    context_text = build_context_text(messages, summary=req.summary)

    previous_question = None
    user_response = None
    if len(messages) >= 2 and messages[-2]["role"] == "assistant" and messages[-1]["role"] == "user":
        previous_question = messages[-2]["content"]
        user_response = messages[-1]["content"]

    tasks = [
        call_agent(
            QUESTION_AGENT_PROMPT.format(
                context=context_text,
                avoid_list="\n".join(f"- {m['content']}" for m in messages if m["role"] == "assistant")
            ),
            stream=False,
            max_tokens=settings.max_tokens_interview_start
        ),
        call_agent(
            FOLLOWUP_AGENT_PROMPT.format(
                previous_question=previous_question or "",
                user_response=user_response or ""
            ),
            stream=False,
            max_tokens=settings.max_tokens_interview_start
        ),
        call_agent(
            FINISH_DECISION_PROMPT.format(
                context=context_text
            ),
            stream=False,
            max_tokens=10
        )
    ]

    question, followup, finish_decision = await asyncio.gather(*tasks)

    # 종료 여부 판단
    finish_raw = finish_decision.strip().lower()
    if finish_raw == "true":
        evaluation = await call_agent(
            EVALUATION_AGENT_PROMPT.format(
                context=context_text
            ),
            stream=True,
            max_tokens=settings.max_tokens_interview_end
        )

        # 🔄 비동기 종료 알림
        asyncio.create_task(notify_interview_end(req.sessionId))

        return evaluation  # ✅ wrap_stream_response 제거
