from src.schemas.chat_schema import FeedbackChatRequest, FeedbackChatResponse
from src.adapters.vllm import generate  # 이제 직접 요청하는 함수
import asyncio  # 비동기 대응

async def handle_feedback_chat(req: FeedbackChatRequest) -> FeedbackChatResponse:
    # 1. 메시지 ChatML 포맷 변환
    messages = [{"role": m.role, "content": m.content} for m in req.messages]

    # 2. 시스템 역할 추가
    messages.insert(0, {
        "role": "system",
        "content": "You are a friendly and helpful AI assistant specialized in code feedback. Be concise, clear, and supportive."
    })

    # 3. LLM 직접 호출 (vLLM)
    # ⚠️ generate는 동기 함수이므로 asyncio 대응 필요
    loop = asyncio.get_event_loop()
    answer = await loop.run_in_executor(None, generate, messages)

    # 4. 응답 구성
    return FeedbackChatResponse(session_id=req.session_id, answer=answer.strip())
