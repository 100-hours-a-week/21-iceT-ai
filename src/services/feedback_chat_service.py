from src.schemas.chat_schema import FeedbackChatRequest, FeedbackChatResponse
from src.adapters.vllm import llm

async def handle_feedback_chat(req: FeedbackChatRequest) -> FeedbackChatResponse:
    # 1. 기존 메시지 변환 (Pydantic → ChatML 포맷)
    messages = [{"role": m.role, "content": m.content} for m in req.messages]

    # 2. ChatML system role 추가 (Qwen에게 역할 부여)
    messages.insert(0, {
        "role": "system",
        "content": "You are a friendly and helpful AI assistant specialized in code feedback. Be concise, clear, and supportive."
    })

    # 3. LLM 호출 (vLLM 서버를 통해 Qwen으로)
    answer = llm.invoke(messages)

    return FeedbackChatResponse(session_id=req.session_id, answer=answer.strip())
