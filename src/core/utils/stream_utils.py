from fastapi.responses import StreamingResponse
from typing import AsyncGenerator

def stream_response(generator: AsyncGenerator[str, None]):
    return StreamingResponse(
        generator,
        media_type="text/event-stream"
    )