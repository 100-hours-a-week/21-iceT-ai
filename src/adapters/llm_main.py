import os
import asyncio
from dotenv import load_dotenv
from src.config import settings

# Gemini 또는 vLLM 선택 여부
USE_GEMINI = os.getenv("USE_GEMINI", "False").lower() == "true"

# 📌 Gemini 분기
if USE_GEMINI:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from src.schemas.solution_schema import SolutionResponse  # 필요 시 교체

    load_dotenv()

    llm = ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        temperature=settings.generation_temperature,
        max_tokens=settings.generation_max_tokens,
        google_api_key=os.getenv("GEMINI_API_KEY")
    )

    structured_llm = llm.with_structured_output(SolutionResponse)

    def to_prompt(prompt_or_messages):
        if isinstance(prompt_or_messages, str):
            return prompt_or_messages
        return "\n".join(f"{m['role'].capitalize()}: {m['content']}" for m in prompt_or_messages if m["role"] != "system")

    async def generate(prompt_or_messages) -> str:
        prompt = to_prompt(prompt_or_messages)
        try:
            response = await asyncio.wait_for(structured_llm.ainvoke(prompt), timeout=60)
            return response.json() if hasattr(response, "json") else str(response)
        except Exception as e:
            raise RuntimeError(f"Gemini 호출 실패: {e}")

# 📌 vLLM 분기
else:
    import httpx

    def to_messages(prompt_or_messages):
        if isinstance(prompt_or_messages, str):
            return [{"role": "user", "content": prompt_or_messages}]
        return prompt_or_messages

    async def generate(prompt_or_messages) -> str:
        messages = to_messages(prompt_or_messages)

        async with httpx.AsyncClient() as client:
            response = await client.post(
                settings.vllm_url,
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
