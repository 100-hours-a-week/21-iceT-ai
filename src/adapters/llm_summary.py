import os
import logging
import json
from openai import OpenAI
from dotenv import load_dotenv
from src.config import settings
from src.schemas.summary_schema import SummaryRequest, SummaryResponse, Summary

load_dotenv()
logger = logging.getLogger(__name__)

client = OpenAI(
    api_key=os.getenv("SOLAR_API_KEY"),
    base_url="https://api.upstage.ai/v1"
)

summary_json_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "type": {"type": "string", "enum": ["problem", "chat"]},
            "speaker": {"type": "string", "enum": ["user", "ai", "system"]},
            "intent": {"type": "string"},
            "content": {"type": "string"},
        },
        "required": ["type", "speaker", "intent", "content"]
    }
}

async def generate_summary(req: SummaryRequest) -> SummaryResponse:
    from src.services.summary_service import build_messages  # 함수 내부에서 import
    try:
        messages = build_messages(req)
        response = client.chat.completions.create(
            model=settings.model_chat,
            temperature=settings.temperature_chat,
            max_tokens=settings.max_tokens_summary,
            messages=messages,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "summary_response",
                    "strict": True,
                    "schema": summary_json_schema,
                }
            }
        )
        content = response.choices[0].message.content
        return SummaryResponse(
            sessionId=req.sessionId,
            summary=[Summary(**s) for s in json.loads(content)]
        )
    except Exception as e:
        logger.error("요약 생성 실패", exc_info=True)
        raise RuntimeError("대화 요약 중 오류가 발생했습니다.") from e
