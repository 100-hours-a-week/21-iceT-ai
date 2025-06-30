import json
from src.config import settings
from src.adapters.llm_feedback import call_feedback_llm
from src.schemas.feedback_schema import FeedbackRequest, FeedbackfollowRequest
from src.core.prompt_templates import FEEDBACK_START_PROMPT, FEEDBACK_ANSWER_PROMPT
from src.core.utils.history_utils import build_context_text
from src.core.utils.stream_utils import wrap_stream_response  # 추가

# 첫 피드백 (start)
async def handle_feedback_start(req: FeedbackRequest):
    prompt = FEEDBACK_START_PROMPT.format(
        problem=req.description,
        code=req.code,
        language=req.codeLanguage,
    )
    return await call_feedback_llm(
        prompt,
        stream=True,
        max_tokens=settings.max_tokens_feedback_start
    )

# 후속 피드백 (answer)
async def handle_feedback_answer(req: FeedbackfollowRequest):
    messages = [{"role": m.role, "content": m.content} for m in req.messages]
    context_text = build_context_text(messages, summary=req.summary)

    prompt = FEEDBACK_ANSWER_PROMPT.format(
        context=context_text,
        user_input=req.messages[-1].content
    )

    return await call_feedback_llm(
        prompt,
        stream=True,
        max_tokens=settings.max_tokens_feedback_answer
    )

