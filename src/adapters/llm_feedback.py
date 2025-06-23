import os
import logging
from openai import OpenAI
from dotenv import load_dotenv
from src.config import settings  # ✅ 설정 import

load_dotenv()
logger = logging.getLogger(__name__)

client = OpenAI(
    api_key=os.getenv("SOLAR_API_KEY"),
    base_url="https://api.upstage.ai/v1"
)

async def call_feedback_llm(prompt: str, stream: bool = True):
    try:
        response = client.chat.completions.create(
            model=settings.model_chat,
            temperature=settings.temperature_chat,
            max_tokens=settings.max_tokens_chat,
            messages=[{"role": "user", "content": prompt}],
            stream=stream
        )

        if stream:
            async def stream_generator():
                for chunk in response:
                    delta = chunk.choices[0].delta
                    if delta and delta.content:
                        yield f"data: {delta.content}\n\n"
            return stream_generator()
        else:
            return response.choices[0].message.content

    except Exception as e:
        logger.error("Feedback LLM 호출 실패", exc_info=True)
        raise RuntimeError("Feedback 응답 생성 중 오류 발생") from e
