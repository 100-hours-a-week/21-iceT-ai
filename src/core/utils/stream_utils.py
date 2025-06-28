from typing import AsyncGenerator

async def wrap_stream_response(response) -> AsyncGenerator[str, None]:
    try:
        async for chunk in response:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                yield f"data: {delta.content}\n\n"
    except Exception as e:
        yield f"data: [ERROR] {str(e)}\n\n"

async def wrap_static_response(text: str) -> AsyncGenerator[str, None]:
    try:
        yield f"data: {text}\n\n"
    except Exception as e:
        yield f"data: [ERROR] {str(e)}\n\n"
