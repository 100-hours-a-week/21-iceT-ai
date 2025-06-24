import json
import asyncio
from json import dumps
from typing import AsyncGenerator
from src.config import settings
from src.adapters.llm_interview import call_agent
from src.schemas.interview_schema import (
    InterviewStartRequest,
    InterviewfollowRequest
)
from src.core.prompt_templates import (
    INTERVIEW_START_PROMPT
)

from src.core.prompt_templates import (
    QUESTION_AGENT_PROMPT,
    FOLLOWUP_AGENT_PROMPT,
    FINISH_DECISION_PROMPT,
    EVALUATION_AGENT_PROMPT
)
from src.core.utils.history_utils import build_context

def extract_problem_and_chat(summary_json: str):
    problem_summary = []
    chat_summary = []
    try:
        items = json.loads(summary_json)
        for item in items:
            if item.get("type") == "problem":
                problem_summary.append(item["content"])
            elif item.get("type") == "chat":
                chat_summary.append(item)
    except Exception:
        pass
    return problem_summary, chat_summary


# ✅ /interview/start
async def handle_interview_start(req: InterviewStartRequest):
    problem_text = f"{req.title}\n{req.description}\n입력: {req.inputRule}\n출력: {req.outputRule}\n예시: {req.inputExample} → {req.outputExample}"
    prompt = INTERVIEW_START_PROMPT.format(
        problem=problem_text,
        language=req.codeLanguage
    )
    return await call_agent(
        prompt,
        stream=True,
        max_tokens=settings.max_tokens_interview_start  # ✅
    )

# ✅ /interview/answer
async def handle_interview_answer(req: InterviewfollowRequest) -> AsyncGenerator[str, None]:
    messages = [{"role": m.role, "content": m.content} for m in req.messages]
    problem_summary, chat_summary = extract_problem_and_chat(req.summary or "")
    context = build_context(messages, chat_summary)

    # 🧱 context 문자열 생성
    problem_text = "\n".join(f"[문제 요약] {c}" for c in problem_summary)
    dialogue_text = "\n".join(f"{m['role']}: {m['content']}" for m in context)
    full_context = f"{problem_text}\n{dialogue_text}" if problem_text else dialogue_text

    # 📌 직전 assistant 질문과 user 응답
    previous_question = None
    user_response = None
    if len(messages) >= 2 and messages[-2]["role"] == "assistant" and messages[-1]["role"] == "user":
        previous_question = messages[-2]["content"]
        user_response = messages[-1]["content"]

    # ⏱️ 병렬 실행 준비
    tasks = [
        call_agent(
            QUESTION_AGENT_PROMPT.format(
                context=full_context,
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
                context=full_context
            ),
            stream=False,
            max_tokens=10
        )
    ]

    question, followup, finish_decision = await asyncio.gather(*tasks)

    # 종료 여부 판단 문자열 정제
    finish_raw = finish_decision.strip().lower()

    # 인터뷰 종료 여부 판단
    if finish_raw == "true":
        evaluation = await call_agent(
            EVALUATION_AGENT_PROMPT.format(
                context=full_context
            ),
            stream=True,
            max_tokens=settings.max_tokens_interview_end
        )

        # 평가는 스트리밍 전송
        async def evaluation_stream():
            async for chunk in evaluation:
                if not chunk.startswith("data: "):
                    continue
                content = chunk.removeprefix("data: ").strip()
                yield f"data: {dumps({'is_finished': True, 'content': content})}\n\n"
        return evaluation_stream()

    # 종료가 아닌 경우 → 꼬리질문 우선 → 질문 fallback
    selected = followup.strip() if followup.strip() else question.strip()

    async def stream_single():
        yield f"data: {dumps({'is_finished': False, 'content': selected})}\n\n"
    return stream_single()
