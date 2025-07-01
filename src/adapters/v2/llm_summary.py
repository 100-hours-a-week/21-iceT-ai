import os, logging
from openai import OpenAI
from dotenv import load_dotenv
from src.config import settings
from src.core.llm_key_manager import APIKeyManager
from src.schemas.v2.summary_schema import SummaryRequest, SummaryResponse

load_dotenv()
logger = logging.getLogger(__name__)

solar_key_manager = APIKeyManager(os.getenv("SOLAR_API_KEYS"))

async def generate_summary(req: SummaryRequest) -> SummaryResponse:
    try:
        client = OpenAI(
            api_key=solar_key_manager.next_key(),
            base_url="https://api.upstage.ai/v1"
        )
        
        messages = messages(req)
        response = client.chat.completions.create(
            model=settings.model_chat,
            temperature=settings.temperature_chat,
            max_tokens=settings.max_tokens_summary,
        )
        content = response.choices[0].message.content
        return SummaryResponse(
            sessionId=req.sessionId,
            summary=content.strip()
        )
    except Exception as e:
        logger.error("요약 생성 실패", exc_info=True)
        raise RuntimeError("대화 요약 중 오류가 발생했습니다.") from e