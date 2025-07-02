import asyncio
from typing import AsyncGenerator

# stream_utils.py
async def wrap_stream_response(response, session_id: str = None) -> AsyncGenerator[str, None]:
    buffer = ""
    try:
        for chunk in response:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                buffer += delta.content
                for line in delta.content.splitlines(keepends=False):
                    # 빈 줄도 명시적으로 처리
                    if line.strip() == " ":
                        yield "data: \n\n"  # 명시적으로 빈 data
                    else:
                        yield f"data: {line}\n\n"
                await asyncio.sleep(0)
    except Exception as e:
        yield f"data: [ERROR] {str(e)}\n\n"