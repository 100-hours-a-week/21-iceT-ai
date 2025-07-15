import asyncio
import re
from typing import AsyncGenerator
from langsmith.client import Client

client = Client()

async def wrap_stream_response(response, session_id: str = None, prompt: str = "", name: str = "streamed-response") -> AsyncGenerator[str, None]:
    import time
    buffer = ""
    line_buf = ""
    full_output = ""
    start_time = time.time()
    first_response_time = None

    try:
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

        last_token_was_newline = False

        while True:
            try:
                chunk = await next_chunk() if is_async else next_chunk()
                if first_response_time is None:
                    first_response_time = time.time()
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
                        if not last_token_was_newline:
                            yield "data: \\n\n\n"
                            last_token_was_newline = True
                    else:
                        tokens = re.findall(r"\S+|\s+|\n", line)
                        for token in tokens:
                            if token == "\n":
                                if not last_token_was_newline:
                                    yield "data: \\n\n\n"
                                    last_token_was_newline = True
                            elif token.isspace():
                                yield f"data: {token}\n\n"
                                last_token_was_newline = False
                            else:
                                yield f"data: {token}\n\n"
                                last_token_was_newline = False
                if is_async:
                    await asyncio.sleep(0)

        # 남은 줄 처리
        if line_buf.strip():
            if re.match(r"^#+\s", line_buf):
                yield f"data: {line_buf}\n\n"
                if not last_token_was_newline:
                    yield "data: \\n\n\n"
                    last_token_was_newline = True
            else:
                tokens = re.findall(r"\S+|\s+|\n", line_buf)
                for token in tokens:
                    if token == "\n":
                        if not last_token_was_newline:
                            yield "data: \\n\n\n"
                            last_token_was_newline = True
                    elif token.isspace():
                        yield f"data: {token}\n\n"
                        last_token_was_newline = False
                    else:
                        yield f"data: {token}\n\n"
                        last_token_was_newline = False

    except Exception as e:
        yield f"data: [ERROR] {str(e)}\n\n"
    finally:
        end_time = time.time()
        if first_response_time:
            print(f"[STREAM] 요청→첫응답: {first_response_time - start_time:.3f}초")
        print(f"[STREAM] 전체 소요 시간: {end_time - start_time:.3f}초")
        try:
            run = client.create_run(
                name=name,
                run_type="llm",
                inputs={"prompt": prompt},
                outputs={"output": full_output},
                metadata={"session_id": session_id or "unknown"}
            )
            if run is not None:
                if asyncio.iscoroutinefunction(run.end):
                    await run.end(outputs={"output": full_output})
                else:
                    run.end(outputs={"output": full_output})
            else:
                print("[LangSmith run 생성 실패] run is None")
        except Exception as e:
            print(f"[LangSmith run 종료 오류] {e}")
        yield "data: [DONE]\n\n"