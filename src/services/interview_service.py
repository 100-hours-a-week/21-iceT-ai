import json
from typing import AsyncGenerator
from src.config import settings
from src.adapters.llm_interview import call_agent, AGENTS
from src.schemas.interview_schema import (
    InterviewStartRequest,
    InterviewfollowRequest,
    InterviewEndRequest
)
from src.core.prompt_templates import (
    INTERVIEW_START_PROMPT,
    INTERVIEW_AGENT_PROMPT,
    INTERVIEW_END_PROMPT,
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
async def handle_interview_answer(req: InterviewfollowRequest):
    messages = [{"role": m.role, "content": m.content} for m in req.messages]

    # 요약에서 problem/chat 분리
    problem_summary, chat_summary = extract_problem_and_chat(req.summary or "")

    # context 생성
    context = build_context(messages, chat_summary)

    # 문제 요약 + 대화 흐름 합치기
    problem_text = "\n".join(f"[문제 요약] {c}" for c in problem_summary)
    dialogue_text = "\n".join(f"{m['role']}: {m['content']}" for m in context)
    full_context = f"{problem_text}\n{dialogue_text}" if problem_text else dialogue_text

    # 프롬프트 생성
    prompt = INTERVIEW_AGENT_PROMPT.format(
        agent_role="인터뷰 시뮬레이터",
        context=full_context
    )

    previous_questions = [
        m["content"] for m in messages if m["role"] == "assistant"
    ]
    if previous_questions:
        avoid_list = "\n".join(f"- {q}" for q in previous_questions)
        prompt += f"\n\n이전 질문과 겹치지 않도록 아래 질문을 피하세요:\n{avoid_list}"

    return await call_agent(
        prompt,
        stream=True,
        max_tokens=settings.max_tokens_interview_start
    )


# ✅ /interview/end
async def handle_interview_end(req: InterviewEndRequest) -> AsyncGenerator[str, None]:
    # 문제/대화 요약 추출
    problem_summary, chat_summary = extract_problem_and_chat(req.summary or "")

    context_list = build_context(
        [{"role": m.role, "content": m.content} for m in req.messages],
        chat_summary
    )
    problem_text = "\n".join(f"[문제 요약] {c}" for c in problem_summary)
    dialogue_text = "\n".join(f"{m['role']}: {m['content']}" for m in context_list)
    full_context = f"{problem_text}\n{dialogue_text}" if problem_text else dialogue_text

    # 개별 에이전트 평가 수집
    agent_results = []
    for agent in AGENTS:
        prompt = INTERVIEW_AGENT_PROMPT.format(
            agent_role=agent,
            context=full_context
        )
        response = await call_agent(
            prompt,
            stream=False,
            max_tokens=settings.max_tokens_interview_answer
        )
        agent_results.append((agent, response))

    combined = "\n\n".join(
        f"### {agent}\n{result}" for agent, result in agent_results
    )

    leader_prompt = f"""
당신은 모든 인터뷰 평가 에이전트의 결과를 종합하는 리더 에이전트입니다.

각 에이전트의 평가 결과를 참고하여 아래 마크다운 양식에 따라 종합 피드백을 작성하세요:

{combined}

---

## ✅ 인터뷰 평가 종합

### 👍 잘한 점
...

### 👎 부족했던 점
...

### 🛠️ 개선 사항
...
"""
    return await call_agent(
        leader_prompt,
        stream=True,
        max_tokens=settings.max_tokens_interview_end
    )



