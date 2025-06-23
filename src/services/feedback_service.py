# src/services/feedback_service.py

import json
from src.adapters.llm_feedback import call_feedback_llm
from src.schemas.feedback_schema import FeedbackRequest, FeedbackfollowRequest
from src.core.prompt_templates import FEEDBACK_START_PROMPT, FEEDBACK_ANSWER_PROMPT
from src.core.utils.history_utils import build_context

# ➤ 첫 피드백 (start)
async def handle_feedback_start(req: FeedbackRequest):
    prompt = FEEDBACK_START_PROMPT.format(
        problem=req.description,
        code=req.code,
        language=req.codeLanguage,
    )
    return await call_feedback_llm(prompt, stream=True)

# ➤ 후속 피드백 (answer)
async def handle_feedback_answer(req: FeedbackfollowRequest):
    # 1. 메시지 파싱
    messages = [{"role": m.role, "content": m.content} for m in req.messages]

    # 2. 요약 파싱 (json str → dict)
    summary = []
    if req.summary:
        try:
            summary = json.loads(req.summary)
        except Exception:
            pass

    # 3. context 생성
    context = build_context(messages, summary)

    # 4. prompt 생성
    prompt = FEEDBACK_ANSWER_PROMPT.format(
        context="\n".join(f"{m['role']}: {m['content']}" for m in context),
        user_input=req.messages[-1].content
    )

    return await call_feedback_llm(prompt, stream=True)

