import logging
from src.adapters.llm_summary import generate_summary
from src.schemas.summary_schema import SummaryRequest, SummaryResponse
from src.core.utils.chat_logger import append_chat_summary

logger = logging.getLogger(__name__)

# 프롬프트 빌더 함수
def build_messages(req: SummaryRequest) -> list:
    messages_str = "\n".join(f"{m.role}: {m.content}" for m in req.messages)

    return [
        {
            "role": "system",
            "content": (
                "당신은 문제 정보와 대화 목록을 요약하는 AI입니다.\n"
                "- 'type' 필드로 'problem' 또는 'chat'을 구분하세요.\n"
                "- 'speaker', 'intent', 'content' 필드도 반드시 포함하세요.\n"
                "- 문제 요약은 반드시 'type': 'problem', 'speaker': 'system' 으로 시작해야 합니다.\n"
                f"- 최대 {req.maxSentences} 문장으로 요약하세요."
            )
        },
        {
            "role": "user",
            "content": f"다음은 문제 설명과 사용자/AI 간의 대화입니다:\n{messages_str}"
        }
    ]

# 대화 요약 서비스 함수
async def summarize_chat(req: SummaryRequest) -> SummaryResponse:
    result = await generate_summary(req)  # ✅ messages 안 만들고 req 그대로 넘김

    try:
        from src.core.utils.chat_logger import append_chat_summary
        append_chat_summary(
            session_id=result.sessionId,
            summary=str(result.summary)  # ✅ static_summary 제거
        )
    except Exception as e:
        logger.warning("요약 CSV 저장 실패: %s", str(e), exc_info=True)

    return result
