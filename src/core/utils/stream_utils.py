import asyncio
from typing import AsyncGenerator

async def wrap_stream_response(response) -> AsyncGenerator[str, None]:
    buffer = ""  # 전체 응답 누적 버퍼
    try:
        for chunk in response:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                buffer += delta.content  # 누적
                await asyncio.sleep(0)
                yield f"data: {delta.content}\n\n"

        # ✅ 스트리밍 종료 후 전체 출력
        print("\n\n [FULL STREAM OUTPUT] \n")
        print(buffer)

    except Exception as e:
        yield f"data: [ERROR] {str(e)}\n\n"

async def wrap_static_response(text: str) -> AsyncGenerator[str, None]:
    try:
        yield f"data: {text}\n\n"
    except Exception as e:
        yield f"data: [ERROR] {str(e)}\n\n"
