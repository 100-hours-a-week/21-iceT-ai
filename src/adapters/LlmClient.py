import openai
from Config import settings

# OpenAI 클라이언트 초기화
openai.api_key = settings.openai_api_key


def generateSolution(prompt: str) -> str:
    """
    OpenAI ChatCompletion 단일 호출 (스트리밍 없이)
    """
    response = openai.ChatCompletion.create(
        model=settings.model_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=settings.temperature,
        max_tokens=settings.max_tokens,
    )
    return response.choices[0].message.content
