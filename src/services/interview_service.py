from src.adapters.vllm import generate
from src.schemas.interview_schema import *
from src.core.prompt_templates import *
import json

# 1. 첫 질문
async def generate_first_question(req: InterviewStartRequest) -> InterviewStartResponse:
    user_prompt = INTERVIEW_START_PROMPT.format(**req.model_dump())

    messages = [
        {"role": "system", "content": "You are a mock technical interviewer. Generate thoughtful questions based on the problem."},
        {"role": "user", "content": user_prompt}
    ]

    output = generate(messages)
    return InterviewStartResponse(title=req.title, question=output.strip())

# 2. 꼬리 질문
async def generate_followup_question(req: InterviewAnswerRequest) -> InterviewAnswerResponse:
    chatml_history = [{"role": m.role, "content": m.content} for m in req.messages]

    chatml_history.insert(0, {
        "role": "system",
        "content": "You are a mock technical interviewer. Ask only one follow-up question based on the previous answer."
    })

    question = generate(chatml_history)
    return InterviewAnswerResponse(session_id=req.session_id, question=question.strip())

# 3. 총평
async def generate_interview_review(req: InterviewEndRequest) -> InterviewEndResponse:
    chatml_history = [{"role": m.role, "content": m.content} for m in req.messages]

    chatml_history.insert(0, {
        "role": "system",
        "content": "You are a technical interviewer. Summarize the interview in the following JSON format only:\n"
                   '{ "good": [...], "bad": [...], "improvement": [...] }'
    })

    raw_output = generate(chatml_history)

    try:
        parsed = json.loads(raw_output)
        return InterviewEndResponse(review=InterviewReview(**parsed))
    except Exception as e:
        raise ValueError(f"총평 JSON 파싱 실패: {e}\n출력:\n{raw_output}")
