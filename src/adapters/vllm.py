import httpx
from src.config import settings


# str 입력도 메시지 리스트로 변환
def to_messages(prompt_or_messages):
    if isinstance(prompt_or_messages, str):
        return [{"role": "user", "content": prompt_or_messages}]
    return prompt_or_messages


# vLLM 서버 호출
async def generate(prompt_or_messages) -> str:
    messages = to_messages(prompt_or_messages)

    async with httpx.AsyncClient() as client:
        response = await client.post(
            settings.vllm_url,  # 주소를 config에서 관리
            json={
                "model": settings.model,
                "messages": messages,
                "temperature": settings.temperature,
                "max_tokens": settings.max_tokens,
                "top_p": 0.9
            },
            timeout=30.0
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
