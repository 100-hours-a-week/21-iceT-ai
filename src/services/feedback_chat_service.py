from src.schemas.chat_schema import FeedbackChatRequest, FeedbackChatResponse
from src.adapters.llm_client import llm  # with_structured_output 아닌 기본 LLM 사용
from src.core.prompt_templates import FEEDBACK_CHAT_PROMPT

async def handle_feedback_chat(req: FeedbackChatRequest) -> FeedbackChatResponse:
    history = ""
    for m in req.messages[:-1]:
        role = "사용자" if m.role == "user" else "AI"
        history += f"{role}: {m.content}\n"
    
    user_input = req.messages[-1].content
    prompt = FEEDBACK_CHAT_PROMPT.format(history=history, user_input=user_input)
    answer = llm.invoke(prompt)
    
    return FeedbackChatResponse(session_id=req.session_id, answer=answer)
