# src/adapters/llm_summary.py

import json
import httpx
from typing import List
from openai import OpenAI

from src.config import settings
from src.schemas.summary_schema import TurnSummaryResponse, TurnSummary


def to_prompt(messages: List[dict]) -> str:
    return "\n".join(
        f"{m['role'].capitalize()}: {m['content']}"
        for m in messages
        if m["role"] in {"user", "assistant"}
    )


# ✅ 요약 생성 분기 (Upstage vs vLLM)
async def generate_summary(messages: List[dict], session_id: str) -> TurnSummaryResponse:
    if not settings.use_vllm:
        return await generate_summary_from_upstage(messages, session_id)
    else:
        return await generate_summary_from_vllm(messages, session_id)


# ✅ Upstage 요약 호출 (Structured Output)
async def generate_summary_from_upstage(
    messages: List[dict], session_id: str
) -> TurnSummaryResponse:
    client = OpenAI(
        api_key=settings.upstage_api_key,
        base_url=settings.upstage_base_url
    )

    base_schema = TurnSummary.model_json_schema()

    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "TurnSummaryResponse",
            "description": "요약 응답",
            "strict": True,
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": base_schema["properties"],
                    "required": ["speaker", "intent", "content"],
                    "additionalProperties": False
                }
            }
        }
    }

    try:
        response = client.chat.completions.create(
            model=settings.upstage_summary_model,
            messages=messages,
            response_format=response_format,
            temperature=settings.summary_temperature,
            max_tokens=settings.summary_max_tokens,
        )

        raw_content = response.choices[0].message.content.strip()
        parsed = json.loads(raw_content)
        structured = [TurnSummary(**item) for item in parsed]

        return TurnSummaryResponse(sessionId=session_id, summary=structured)

    except Exception as e:
        raise RuntimeError(f"Upstage 요약 실패: {e}")


# ✅ vLLM 요약 호출 (plain JSON 반환)
async def generate_summary_from_vllm(
    messages: List[dict], session_id: str
) -> TurnSummaryResponse:
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

        raw_content = response.json()["choices"][0]["message"]["content"].strip()
        parsed = json.loads(raw_content)
        structured = [TurnSummary(**item) for item in parsed]

        return TurnSummaryResponse(sessionId=session_id, summary=structured)
