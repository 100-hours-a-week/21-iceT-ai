from src.schemas.chat_schema import FeedbackChatRequest, FeedbackChatResponse
from src.adapters.vllm import generate  # 비동기 함수

async def handle_feedback_chat(req: FeedbackChatRequest) -> FeedbackChatResponse:
    # ChatML 포맷 변환
    messages = [{"role": m.role, "content": m.content} for m in req.messages]

    # system 역할 추가
    messages.insert(0, {
        "role": "system",
        "content": "You are a friendly and helpful AI assistant specialized in code feedback. Be concise, clear, and supportive."
    })

    # 비동기 호출
    answer = await generate(messages)

    return FeedbackChatResponse(sessionId=req.sessionId, answer=answer.strip())
