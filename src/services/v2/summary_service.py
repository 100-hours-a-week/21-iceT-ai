import logging
import asyncio
from typing import List
from src.config import settings
from adapters.v2.llm_summary import generate_summary
from schemas.v2.summary_schema import SummaryRequest, SummaryResponse
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
                "- 문제 요약과 대화 요약을 구분하여 하나의 긴 텍스트로 출력하세요.\n"
                "- 각 항목에는 반드시 요약된 발화 내용이 포함되어야 합니다.\n"
                f"- 문제 정보는 최대 {settings.max_summary_sentences_problem}문장, "
                f"대화 요약은 최대 {settings.max_summary_sentences_chat}문장으로 정리하세요.\n"
                "- 두 영역은 명확히 구분되며, 통합 텍스트로 구성되어야 합니다."
            )
        },
        {
            "role": "user",
            "content": f"다음은 문제 설명과 사용자/AI 간의 대화입니다:\n{messages_str}"
        }
    ]

# 대화 요약 서비스 함수
async def summarize_chat(requests: List[SummaryRequest]) -> List[SummaryResponse]:
    async def process_one(req: SummaryRequest) -> SummaryResponse:
        result = await generate_summary(req)
        try:
            append_chat_summary(
                session_id=result.sessionId,
                summary=result.summary
            )
        except Exception as e:
            logger.warning("요약 CSV 저장 실패: %s", str(e), exc_info=True)
        return result

    tasks = [process_one(r) for r in requests]
    return await asyncio.gather(*tasks)