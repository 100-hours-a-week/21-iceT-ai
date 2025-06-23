import json
from typing import AsyncGenerator
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

# ✅ /interview/start
async def handle_interview_start(req: InterviewStartRequest):
    problem_text = f"{req.title}\n{req.description}\n입력: {req.inputRule}\n출력: {req.outputRule}\n예시: {req.inputExample} → {req.outputExample}"
    prompt = INTERVIEW_START_PROMPT.format(
        problem=problem_text,
        language=req.codeLanguage
    )
    return await call_agent(prompt, stream=True)

# ✅ /interview/answer
async def handle_interview_answer(req: InterviewfollowRequest):
    messages = [{"role": m.role, "content": m.content} for m in req.messages]

    summary_data = []
    if req.summary:
        try:
            summary_data = json.loads(req.summary)
        except Exception:
            pass

    context = build_context(messages, summary_data)

    previous_questions = [
        m["content"] for m in messages if m["role"] == "assistant"
    ]

    prompt = INTERVIEW_AGENT_PROMPT.format(
        agent_role="인터뷰 시뮬레이터",
        context="\n".join(f"{m['role']}: {m['content']}" for m in context)
    )
    if previous_questions:
        avoid_list = "\n".join(f"- {q}" for q in previous_questions)
        prompt += f"\n\n이전 질문과 겹치지 않도록 아래 질문을 피하세요:\n{avoid_list}"

    return await call_agent(prompt, stream=True)

# ✅ /interview/end
async def handle_interview_end(req: InterviewEndRequest) -> AsyncGenerator[str, None]:
    context = "\n".join(f"{m.role}: {m.content}" for m in req.messages)

    agent_results = []
    for agent in AGENTS:
        prompt = INTERVIEW_AGENT_PROMPT.format(
            agent_role=agent,
            context=context
        )
        response = await call_agent(prompt, stream=False)
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
    return await call_agent(leader_prompt, stream=True)

