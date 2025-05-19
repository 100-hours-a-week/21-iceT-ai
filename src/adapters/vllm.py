import requests
import aiohttp
from src.config import settings

# ✅ 동기 방식
def generate(prompt_or_messages):
    if isinstance(prompt_or_messages, str):
        prompt_or_messages = [{"role": "user", "content": prompt_or_messages}]

    if not any(m["role"] == "system" for m in prompt_or_messages):
        prompt_or_messages.insert(0, {
            "role": "system",
            "content": "You are a helpful assistant."
        })

    body = {
        "model": settings.model,
        "messages": prompt_or_messages,
        "temperature": settings.temperature,
        "max_tokens": settings.max_tokens,
        "top_p": 0.9
    }

    response = requests.post("http://localhost:8001/v1/chat/completions", json=body)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

# ✅ 비동기 방식
async def generate_async(prompt_or_messages):
    if isinstance(prompt_or_messages, str):
        prompt_or_messages = [{"role": "user", "content": prompt_or_messages}]

    if not any(m["role"] == "system" for m in prompt_or_messages):
        prompt_or_messages.insert(0, {
            "role": "system",
            "content": "You are a helpful assistant."
        })

    body = {
        "model": settings.model,
        "messages": prompt_or_messages,
        "temperature": settings.temperature,
        "max_tokens": settings.max_tokens,
        "top_p": 0.9
    }

    async with aiohttp.ClientSession() as session:
        async with session.post("http://localhost:8001/v1/chat/completions", json=body) as resp:
            if resp.status != 200:
                raise ValueError(f"❌ vLLM 요청 실패: {resp.status}")
            result = await resp.json()
            return result["choices"][0]["message"]["content"]
