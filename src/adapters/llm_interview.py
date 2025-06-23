import os
import logging
from openai import OpenAI
from dotenv import load_dotenv
from src.config import settings

load_dotenv()
logger = logging.getLogger(__name__)

client = OpenAI(
    api_key=os.getenv("SOLAR_API_KEY"),
    base_url="https://api.upstage.ai/v1"
)

AGENTS = [
    "전략 분석 에이전트",
    "복잡도 평가 에이전트",
    "테스트 케이스 에이전트",
    "코드품질 에이전트",
    "인터뷰 시뮬레이터",
    "대안 탐색 에이전트",
    "에러 핸들링 에이전트"
]

async def call_agent(prompt: str, stream: bool = True):
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
        logger.error("Interview Agent 호출 실패", exc_info=True)
        raise RuntimeError("인터뷰 에이전트 응답 생성 실패") from e
