import asyncio
import logging
import httpx
import json
from openai import OpenAI
from pydantic import BaseModel
from typing import AsyncGenerator

from src.config import settings
from src.adapters.llm_parsers import (
    SCHEMA_PARSERS,
    parse_json_from_llm_output
)

logger = logging.getLogger(__name__)

def to_messages(prompt_or_messages):
    if isinstance(prompt_or_messages, str):
        return [{"role": "user", "content": prompt_or_messages}]
    return prompt_or_messages

# 파일 상단 import 추가
from typing import AsyncGenerator

# 새로운 함수 추가
async def stream_generate(prompt_or_messages) -> AsyncGenerator[str, None]:
    messages = to_messages(prompt_or_messages)

    # Upstage OpenAI client
    client = OpenAI(
        api_key=settings.upstage_api_key,
        base_url="https://api.upstage.ai/v1"
    )

    # 스트리밍 호출
    stream = client.chat.completions.create(
        model=settings.upstage_model,
        messages=messages,
        temperature=settings.chat_temperature,
        max_tokens=settings.chat_max_tokens,
        stream=True  # ✅ 핵심 옵션
    )

    # 스트리밍된 토큰을 하나씩 yield
    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content



# ✅ Upstage / vLLM 공통 호출 인터페이스
async def generate(prompt_or_messages, schema_class: type[BaseModel] = None, original_input=None) -> BaseModel | str:
    messages = to_messages(prompt_or_messages)

    # ✅ Upstage structured output
    if settings.use_upstage:
        client = OpenAI(
            api_key=settings.upstage_api_key,
            base_url="https://api.upstage.ai/v1"
        )

        if schema_class is None:
            raise ValueError("Upstage 호출 시 schema_class는 필수입니다.")

        base_schema = schema_class.model_json_schema()
        core_schema = {
            "type": "object",
            "properties": base_schema["properties"],
            "required": base_schema.get("required", []),
            "additionalProperties": False
        }

        response_format = {
            "type": "json_schema",
            "json_schema": {
                "name": schema_class.__name__,
                "description": f"{schema_class.__name__} structured output",
                "strict": True,
                "schema": core_schema
            }
        }

        try:
            response = client.chat.completions.create(
                model=settings.upstage_model,
                messages=messages,
                response_format=response_format,
                temperature=settings.chat_temperature,
                max_tokens=settings.chat_max_tokens
            )
            content = response.choices[0].message.content
            return schema_class.model_validate_json(content)
        except Exception as e:
            logger.error("Upstage 호출 실패", exc_info=True)
            raise RuntimeError("LLM structured output 생성 중 오류가 발생했습니다.") from e

    # ✅ vLLM fallback: 일반 JSON 응답 파싱
    else:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                settings.vllm_url,
                json={
                    "model": settings.vllm_model,
                    "messages": messages,
                    "temperature": settings.chat_temperature,
                    "max_tokens": settings.chat_max_tokens,
                    "top_p": 0.9
                },
                timeout=120.0
            )
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]

            if schema_class is None:
                return content  # 자유 응답형 (예: answer)

            if schema_class in SCHEMA_PARSERS:
                return SCHEMA_PARSERS[schema_class](content, original_input)
            else:
                parsed = parse_json_from_llm_output(content)
                return schema_class(**parsed)