import asyncio
from typing import AsyncGenerator

async def wrap_stream_response(response, session_id: str = None) -> AsyncGenerator[str, None]:
    buffer = ""
    try:
        for chunk in response:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                buffer += delta.content
                await asyncio.sleep(0)
                yield f"data: {delta.content}\n\n"

    except Exception as e:
        yield f"data: [ERROR] {str(e)}\n\n"