import asyncio
import logging
import httpx
import os
import json
from openai import OpenAI
from src.config import settings
from src.schemas.solution_schema import SolutionResponse

logger = logging.getLogger(__name__)

def to_messages(prompt_or_messages):
    if isinstance(prompt_or_messages, str):
        return [{"role": "user", "content": prompt_or_messages}]
    return prompt_or_messages


# ✅ 분기 방식: Upstage vs vLLM
async def generate(prompt_or_messages) -> SolutionResponse:
    messages = to_messages(prompt_or_messages)

    if settings.use_upstage:
        print(f"✅ [DEBUG] 사용 모델 이름: {settings.model}")
        print(f"✅ [DEBUG] Upstage 사용 중 / API_KEY={settings.upstage_api_key[:10]}...")
        # 🔶 Upstage 클라이언트
        client = OpenAI(
            api_key=settings.upstage_api_key,
            base_url="https://api.upstage.ai/v1"
        )

        # structured output 요구
        response_format = {
            "type": "json_schema",
            "json_schema": SolutionResponse.model_json_schema()
        }

        try:
            response = client.chat.completions.create(
                model=settings.model,
                messages=messages,
                response_format=response_format,
                temperature=settings.generation_temperature,
                max_tokens=settings.generation_max_tokens,
            )
            content = response.choices[0].message.content
            return SolutionResponse.model_validate_json(content)
        except Exception as e:
            logger.error("Upstage 호출 실패", exc_info=True)
            raise RuntimeError("해설 생성 중 오류가 발생했습니다.") from e

    else:
        # 🔷 기존 vLLM 서버 호출
        async with httpx.AsyncClient() as client:
            response = await client.post(
                settings.vllm_url,
                json={
                    "model": settings.vllm_model,
                    "messages": messages,
                    "temperature": settings.generation_temperature,
                    "max_tokens": settings.generation_max_tokens,
                    "top_p": 0.9
                },
                timeout=30.0
            )
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            return SolutionResponse.model_validate_json(content)
