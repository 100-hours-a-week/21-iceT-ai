import asyncio
import json
import httpx
from openai import OpenAI
from typing import AsyncGenerator

from src.config import settings
from src.adapters.llm_key_manager import api_key_manager
from src.adapters.llm_parsers import estimate_tokens


llm_semaphore = asyncio.Semaphore(10)


def to_messages(prompt_or_messages):
    if isinstance(prompt_or_messages, str):
        return [{"role": "user", "content": prompt_or_messages}]
    return prompt_or_messages


# ✅ 통합 스트리밍 함수
async def stream_generate(prompt_or_messages) -> AsyncGenerator[str, None]:
    messages = to_messages(prompt_or_messages)

    async with llm_semaphore:
        if not settings.use_vllm:
            # ▶ Upstage
            key = api_key_manager.select_least_busy_key()
            client = OpenAI(
                api_key=key,
                base_url="https://api.upstage.ai/v1"
            )

            stream = client.chat.completions.create(
                model=settings.upstage_model,
                messages=messages,
                temperature=settings.chat_temperature,
                max_tokens=settings.chat_max_tokens,
                stream=True
            )

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

            api_key_manager.record_usage(key, estimate_tokens(messages))

        else:
            # ▶ vLLM (Qwen 등)
            async with httpx.AsyncClient() as client:
                async with client.stream(
                    "POST",
                    settings.vllm_url,
                    json={
                        "model": settings.vllm_model,
                        "messages": messages,
                        "temperature": settings.chat_temperature,
                        "max_tokens": settings.chat_max_tokens,
                        "stream": True,
                    },
                    timeout=120.0
                ) as response:
                    async for line in response.aiter_lines():
                        if line.startswith("data:"):
                            content = line.removeprefix("data:").strip()
                            if content and content != "[DONE]":
                                try:
                                    chunk = json.loads(content)
                                    delta = chunk["choices"][0]["delta"].get("content")
                                    if delta:
                                        yield delta
                                except Exception:
                                    continue
