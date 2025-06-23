import json
from src.config import settings
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
    return await call_feedback_llm(
        prompt,
        stream=True,
        max_tokens=settings.max_tokens_feedback_start
    )

# ➤ 후속 피드백 (answer)
import json
from src.config import settings
from src.adapters.llm_feedback import call_feedback_llm
from src.schemas.feedback_schema import FeedbackfollowRequest
from src.core.prompt_templates import FEEDBACK_ANSWER_PROMPT
from src.core.utils.history_utils import build_context

# ➤ 후속 피드백 (answer)
async def handle_feedback_answer(req: FeedbackfollowRequest):
    # 1. 메시지 파싱
    messages = [{"role": m.role, "content": m.content} for m in req.messages]

    # 2. 요약 분리 파싱
    problem_summary = []
    chat_summary = []

    if req.summary:
        try:
            all_items = json.loads(req.summary)
            for item in all_items:
                if item.get("type") == "problem":
                    problem_summary.append(item["content"])
                elif item.get("type") == "chat":
                    chat_summary.append(item)
        except Exception:
            pass

    # 3. context 생성
    context = build_context(messages, chat_summary)

    # 4. context 문자열 조립 (문제 요약 + 대화 흐름)
    problem_text = "\n".join(f"[문제 요약] {c}" for c in problem_summary)
    dialogue_text = "\n".join(f"{m['role']}: {m['content']}" for m in context)
    full_context = f"{problem_text}\n{dialogue_text}" if problem_text else dialogue_text

    # 5. prompt 생성
    prompt = FEEDBACK_ANSWER_PROMPT.format(
        context=full_context,
        user_input=req.messages[-1].content
    )

    # 6. 호출
    return await call_feedback_llm(
        prompt,
        stream=True,
        max_tokens=settings.max_tokens_feedback_answer
    )


