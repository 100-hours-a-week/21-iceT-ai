import asyncio
from typing import AsyncGenerator
from src.core.utils.chat_logger import append_chat_record

async def wrap_stream_response(response, session_id: str = None) -> AsyncGenerator[str, None]:
    buffer = ""
    try:
        for chunk in response:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                buffer += delta.content
                await asyncio.sleep(0)
                yield f"data: {delta.content}\n\n"

        if session_id:
            append_chat_record(session_id, "assistant", buffer)

    except Exception as e:
        yield f"data: [ERROR] {str(e)}\n\n"

import asyncio
from typing import AsyncGenerator
from src.core.utils.chat_logger import append_chat_record

async def wrap_stream_response(response, session_id: str = None) -> AsyncGenerator[str, None]:
    buffer = ""
    try:
        for chunk in response:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                buffer += delta.content
                await asyncio.sleep(0)
                yield f"data: {delta.content}\n\n"

        if session_id:
            append_chat_record(session_id, "assistant", buffer)

    except Exception as e:
        yield f"data: [ERROR] {str(e)}\n\n"