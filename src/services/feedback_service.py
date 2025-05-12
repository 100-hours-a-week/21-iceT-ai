from src.adapters.vllm import generate
from src.schemas.feedback_schema import (
    FeedbackRequest, FeedbackResponse,
    FeedbackAnswerRequest, FeedbackAnswerResponse
)
from src.core.prompt_templates import FEEDBACK_PROMPT
from src.core.llm_utils import parse_feedback_response  # ✅ 추가

# 1. /feedback/start: 코드 피드백 생성
async def explain_feedback(req: FeedbackRequest) -> FeedbackResponse:
    prompt = FEEDBACK_PROMPT.format(**req.model_dump())

    # ✅ ChatML 메시지 구성
    messages = [
        {"role": "system", "content": "You are a professional code reviewer. Always respond in correct JSON."},
        {"role": "user", "content": prompt}
    ]

    raw_output = generate(messages)

    # ✅ 마크다운 제거 및 robust JSON 파싱
    return parse_feedback_response(raw_output, title=req.title)

# 2. /feedback/answer: 챗봇 자유 응답
async def answer_feedback_question(req: FeedbackAnswerRequest) -> FeedbackAnswerResponse:
    # ChatML 형식으로 대화 이력 구성
    messages = [{"role": m.role, "content": m.content} for m in req.messages]

    # 마지막 질문을 user 메시지로 보장
    if not messages or messages[-1]["role"] != "user":
        raise ValueError("마지막 메시지는 반드시 사용자여야 합니다.")

    # system 메시지 앞에 삽입
    messages.insert(0, {
        "role": "system",
        "content": "You are a helpful and kind code review assistant. Respond clearly and concisely."
    })

    output = generate(messages)
    return FeedbackAnswerResponse(session_id=req.session_id, answer=output.strip())