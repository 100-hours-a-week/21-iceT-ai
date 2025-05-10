from src.adapters.vllm import generate
from src.schemas.feedback_schema import (
    FeedbackRequest, FeedbackResponse,
    FeedbackAnswerRequest, FeedbackAnswerResponse
)

# 1. /feedback/start: 코드 피드백 생성
def build_feedback_prompt(req: FeedbackRequest) -> str:
    return f"""
너는 코드 리뷰어야. 아래 문제와 사용자의 코드를 바탕으로,
- 잘한점 2가지
- 개선할 점 2가지
- 개선된 코드

형식은 다음과 같아야 해:

###  잘한점
- ...
- ...

### 개선해야 할 점
- ...
- ...

### 개선된 코드
`코드블럭`

문제 설명:
{req.description}

코드:
{req.code}
"""

async def explain_feedback(req: FeedbackRequest) -> FeedbackResponse:
    prompt = build_feedback_prompt(req)
    raw_output = generate(prompt)

    # 수동 파싱
    try:
        sections = raw_output.split("###")
        good = [line.strip("- ") for line in sections[1].splitlines()[1:] if line.strip()]
        bad = [line.strip("- ") for line in sections[2].splitlines()[1:] if line.strip()]
        code = "\n".join(sections[3].splitlines()[1:])
        return FeedbackResponse(title=req.title, good=good, bad=bad, improved_code=code.strip())
    except Exception as e:
        raise ValueError(f"LLM 응답 파싱 실패: {e}\n출력:\n{raw_output}")


# 2. /feedback/answer: 챗봇 자유 응답
async def answer_feedback_question(req: FeedbackAnswerRequest) -> FeedbackAnswerResponse:
    history = ""
    for m in req.messages:
        prefix = "AI" if m.role == "assistant" else "사용자"
        history += f"{prefix}: {m.content}\n"
    
    prompt = f"""
너는 코드 리뷰를 도와주는 AI야. 아래는 지금까지의 대화야.

{history}

위 대화를 바탕으로 다음 사용자 질문에 대해 자세히 답변해줘.
단, 여는 말이나 맺는 말 없이 바로 답변 내용만 출력해.
"""
    output = generate(prompt)
    return FeedbackAnswerResponse(session_id=req.session_id, answer=output.strip())
