import asyncio
import httpx
from typing import List
from src.config import settings

# Gemini 사용 여부
if settings.use_gemini:
    from langchain_google_genai import ChatGoogleGenerativeAI

    llm = ChatGoogleGenerativeAI(
        model=settings.gemini_model
        temperature=settings.summary_temperature,
        max_tokens=settings.summary_max_tokens,
        google_api_key=settings.gemini_api_key
    )

    def to_prompt(messages: List[dict]) -> str:
        return "\n".join(
            f"{m['role'].capitalize()}: {m['content']}" for m in messages if m["role"] in {"user", "assistant"}
        )

    async def generate_summary_from_cpu_model(messages: List[dict]) -> str:
        prompt = to_prompt(messages)
        try:
            response = await asyncio.wait_for(llm.ainvoke(prompt), timeout=60)
            return str(response)
        except Exception as e:
            raise RuntimeError(f"Gemini 요약 실패: {e}")

# vLLM 서버 사용 (기존 구조)
else:
    async def generate_summary_from_cpu_model(messages: List[dict]) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                settings.summary_llm_url,
                json={
                    "model": settings.summary_model,
                    "messages": messages,
                    "temperature": settings.temperature,
                    "max_tokens": settings.max_tokens
                },
                timeout=60.0
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
