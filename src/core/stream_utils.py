import asyncio
import re
from typing import AsyncGenerator
from langsmith.client import Client

client = Client()

async def wrap_stream_response(response, session_id: str = None, prompt: str = "") -> AsyncGenerator[str, None]:
    buffer = ""
    line_buf = ""
    full_output = ""

    try:
        if hasattr(response, "__aiter__"):
            async for chunk in response:
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    content = delta.content
                    buffer += content
                    line_buf += content
                    full_output += content

                    while "\n" in line_buf:
                        line, line_buf = line_buf.split("\n", 1)
                        tokens = re.findall(r"\S+|\s", line)
                        for token in tokens:
                            if token == " ":
                                yield "data:  \n\n"
                            else:
                                yield f"data: {token}\n\n"
                        yield "data: \\n\n\n"
                    await asyncio.sleep(0)
        else:
            for chunk in response:
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    content = delta.content
                    buffer += content
                    line_buf += content
                    full_output += content

                    while "\n" in line_buf:
                        line, line_buf = line_buf.split("\n", 1)
                        tokens = re.findall(r"\S+|\s", line)
                        for token in tokens:
                            if token == " ":
                                yield "data:  \n\n"
                            else:
                                yield f"data: {token}\n\n"
                        yield "data: \\n\n\n"
                    await asyncio.sleep(0)

        # 남은 줄 처리
        if line_buf.strip():
            tokens = re.findall(r"\S+|\s", line_buf)
            for token in tokens:
                if token == " ":
                    yield "data:  \n\n"
                else:
                    yield f"data: {token}\n\n"

    except Exception as e:
        yield f"data: [ERROR] {str(e)}\n\n"
    finally:
            try:
                run = client.create_run(
                    name="Streamed Response",
                    run_type="llm",
                    inputs={"prompt": prompt},
                    outputs={"output": full_output},
                    metadata={"session_id": session_id or "unknown"}
                )
                run.end(outputs={"output": full_output})
            except Exception:
                pass