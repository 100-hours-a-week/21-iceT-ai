import os
import logging
import json
from openai import OpenAI
from dotenv import load_dotenv
from src.config import settings
from src.schemas.summary_schema import SummaryResponse

load_dotenv()
logger = logging.getLogger(__name__)

client = OpenAI(
    api_key=os.getenv("SOLAR_API_KEY"),
    base_url="https://api.upstage.ai/v1"
)

async def generate_summary(prompt: str) -> SummaryResponse:
    try:
        response = client.chat.completions.create(
            model=settings.model_chat,
            temperature=settings.temperature_chat,
            max_tokens=settings.max_tokens_chat,
            messages=[{"role": "user", "content": prompt}],
            stream=False
        )
        content = response.choices[0].message.content
        return SummaryResponse(**json.loads(content))
    except Exception as e:
        logger.error("요약 생성 실패", exc_info=True)
        raise RuntimeError("대화 요약 중 오류가 발생했습니다.") from e
