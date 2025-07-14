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
        # response가 async iterator 또는 일반 iterator 모두 처리
        iterator = response
        if hasattr(response, "__aiter__"):
            iterator = response.__aiter__()
            async def next_chunk():
                return await iterator.__anext__()
            is_async = True
        else:
            iterator = iter(response)
            def next_chunk():
                return next(iterator)
            is_async = False

        while True:
            try:
                chunk = await next_chunk() if is_async else next_chunk()
            except (StopIteration, StopAsyncIteration):
                break
            delta = chunk.choices[0].delta
            if delta and delta.content:
                content = delta.content
                buffer += content
                line_buf += content
                full_output += content

                while "\n" in line_buf:
                    line, line_buf = line_buf.split("\n", 1)
                    if re.match(r"^#+\s", line):
                        yield f"data: {line}\n\n"
                        if not line_buf.startswith("\n"):
                            yield "data: \\n\n\n"
                    else:
                        tokens = re.findall(r"\S+|\s+", line)
                        last_token_was_newline = False
                        for token in tokens:
                            if token == "\n" or token.isspace():
                                if not last_token_was_newline:
                                    yield "data: \\n\n\n"
                                    last_token_was_newline = True
                            else:
                                yield f"data: {token}\n\n"
                                last_token_was_newline = False
                if is_async:
                    await asyncio.sleep(0)

        # 남은 줄 처리
        if line_buf.strip():
            if re.match(r"^#+\s", line_buf):
                yield f"data: {line_buf}\n\n"
                yield "data: \\n\n\n"
            else:
                tokens = re.findall(r"\S+|\s+", line_buf)
                last_token_was_newline = False
                for token in tokens:
                    if token == "\n" or token.isspace():
                        if not last_token_was_newline:
                            yield "data: \\n\n\n"
                            last_token_was_newline = True
                    else:
                        yield f"data: {token}\n\n"
                        last_token_was_newline = False

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