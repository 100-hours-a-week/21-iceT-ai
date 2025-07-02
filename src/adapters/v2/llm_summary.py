import os, logging
from openai import OpenAI
from dotenv import load_dotenv
from src.config import settings
from src.core.llm_key_manager import APIKeyManager
from src.schemas.v2.summary_schema import SummaryRequest, SummaryResponse

load_dotenv()
logger = logging.getLogger(__name__)

solar_key_manager = APIKeyManager(os.getenv("SOLAR_API_KEYS").split(","))

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

async def generate_summary(req: SummaryRequest) -> SummaryResponse:
    try:
        client = OpenAI(
            api_key=solar_key_manager.next_key(),
            base_url="https://api.upstage.ai/v1"
        )
        
        messages = build_messages(req)
        response = client.chat.completions.create(
            model=settings.model_chat,
            temperature=settings.temperature_chat,
            max_tokens=settings.max_tokens_summary,
            messages=messages
        )
        content = response.choices[0].message.content
        
        return SummaryResponse(
            sessionId=req.sessionId,
            summary=content.strip()
        )
    except Exception as e:
        logger.error("요약 생성 실패", exc_info=True)
        raise RuntimeError("대화 요약 중 오류가 발생했습니다.") from e