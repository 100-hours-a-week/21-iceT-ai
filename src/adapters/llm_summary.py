# src/adapters/llm_summary.py
import asyncio
import httpx
from typing import List
from openai import OpenAI
from src.config import settings


def to_prompt(messages: List[dict]) -> str:
    return "\n".join(
        f"{m['role'].capitalize()}: {m['content']}" for m in messages if m["role"] in {"user", "assistant"}
    )


# ✅ 요약 전용 분기 처리
async def generate_summary(messages: List[dict]) -> str:
    if settings.use_upstage:
        return await generate_summary_from_upstage(messages)
    else:
        return await generate_summary_from_vllm(messages)


# ✅ Upstage 요약 호출
async def generate_summary_from_upstage(messages: List[dict]) -> str:
    client = OpenAI(
        api_key=settings.upstage_api_key,
        base_url=settings.upstage_base_url
    )

    try:
        response = client.chat.completions.create(
            model=settings.upstage_summary_model,
            messages=messages,
            temperature=settings.summary_temperature,
            max_tokens=settings.summary_max_tokens,
        )
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"Upstage 요약 실패: {e}")


# ✅ vLLM 요약 호출
async def generate_summary_from_vllm(messages: List[dict]) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            settings.vllm_summary_url,
            json={
                "model": settings.vllm_summary_model,
                "messages": messages,
                "temperature": settings.summary_temperature,
                "max_tokens": settings.summary_max_tokens
            },
            timeout=240.0
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
