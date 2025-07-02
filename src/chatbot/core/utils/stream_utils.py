import asyncio
import re
from typing import AsyncGenerator

async def wrap_stream_response(response, session_id: str = None) -> AsyncGenerator[str, None]:
    buffer = ""
    line_buf = ""

    try:
        for chunk in response:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                content = delta.content
                buffer += content
                line_buf += content

                # 줄 단위로 먼저 처리
                while "\n" in line_buf:
                    line, line_buf = line_buf.split("\n", 1)
                    tokens = re.findall(r"[^\s]+", line)
                    for token in tokens:
                        yield f"data: {token}\n\n"
                    # 줄바꿈 시 공백 한 칸으로 명시적 표현
                    yield "data:  \n\n"

                await asyncio.sleep(0)

        # 남은 줄 처리
        if line_buf.strip():
            tokens = re.findall(r"[^\s]+", line_buf)
            for token in tokens:
                yield f"data: {token}\n\n"

    except Exception as e:
        yield f"data: [ERROR] {str(e)}\n\n"
