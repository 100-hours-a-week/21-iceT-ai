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

# Upstage 클라이언트 설정
client = OpenAI(
    api_key=settings.upstage_api_key,
    base_url="https://api.upstage.ai/v1"
)

async def generate_summary_from_cpu_model(messages: List[dict]) -> str:
    try:
        response = client.chat.completions.create(
            model=settings.upstage_summary_model,  # 예: "solar-mini" 또는 "solar-pro"
            messages=messages,
            temperature=settings.summary_temperature,
            max_tokens=settings.summary_max_tokens,
        )
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"Upstage 요약 실패: {e}")

"""
    # 기존 vLLM 구조
    async def generate_summary_from_cpu_model(messages: List[dict]) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                settings.summary_llm_url,
                json={
                    "model": settings.summary_model,
                    "messages": messages,
                    "temperature": settings.summary_temperature,
                    "max_tokens": settings.summary_max_tokens
                },
                timeout=60.0
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
"""