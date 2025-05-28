import httpx
from typing import List

# 💡 요약용 CPU 모델 서버 주소 (예: loRA, Qwen Chat 등)
SUMMARY_LLM_URL = "http://localhost:1234/v1/chat/completions"  # 실제 포트에 맞게 수정

async def generate_summary_from_cpu_model(messages: List[dict]) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            SUMMARY_LLM_URL,
            json={
                "model": "qwen1.5-1.8b-chat",  # 요약 전용 이름 (실제와 다르면 변경 필요)
                "messages": messages,
                "temperature": 0.3,
                "max_tokens": 512
            },
            timeout=60.0
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
