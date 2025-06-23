import logging
from src.core.prompt_templates import SUMMARY_PROMPT
from src.adapters.llm_summary import generate_summary
from src.schemas.summary_schema import SummaryRequest, SummaryResponse
from src.core.utils.chat_logger import append_chat_summary

logger = logging.getLogger(__name__)

# 프롬프트 빌더 함수
def build_prompt(req: SummaryRequest) -> str:
    messages_str = "\n".join(
        f"{m.role}: {m.content}" for m in req.messages
    )
    static_summary = req.staticSummary if req.staticSummary else "없음"
    prompt = SUMMARY_PROMPT.invoke(
        {
            "session_id": req.sessionId,
            "messages": messages_str,
            "max_sentences": req.maxSentences,
            "mode": req.mode,
            "static_summary": static_summary,
        }
    )
    return prompt

# 대화 요약 서비스 함수
async def summarize_chat(req: SummaryRequest) -> SummaryResponse:
    prompt = build_prompt(req)
    result = await generate_summary(prompt)

async def summarize_chat(req: SummaryRequest) -> SummaryResponse:
    prompt = build_prompt(req)
    result = await generate_summary(prompt)

    # ✅ 요약 CSV 저장
    append_chat_summary(
        session_id=result.sessionId,
        static_summary=str(result.staticSummary or ""),
        summary=str(result.summary),
    )

    return result