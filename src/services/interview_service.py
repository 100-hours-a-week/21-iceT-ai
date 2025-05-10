from src.adapters.vllm import generate
from src.schemas.interview_schema import *
from src.core.prompt_templates import *

# 1. 첫 질문
async def generate_first_question(req: InterviewStartRequest) -> InterviewStartResponse:
    prompt = INTERVIEW_START_PROMPT.format(**req.model_dump())
    output = generate(prompt)
    return InterviewStartResponse(title=req.title, question=output.strip())

# 2. 꼬리 질문
async def generate_followup_question(req: InterviewAnswerRequest) -> InterviewAnswerResponse:
    history = "\n".join(
        [("면접관" if m.role == "assistant" else "지원자") + ": " + m.content for m in req.messages]
    )
    prompt = INTERVIEW_FOLLOWUP_PROMPT.format(history=history)
    question = generate(prompt)
    return InterviewAnswerResponse(session_id=req.session_id, question=question.strip())

# 3. 총평
async def generate_interview_review(req: InterviewEndRequest) -> InterviewEndResponse:
    history = "\n".join(
        [("면접관" if m.role == "assistant" else "지원자") + ": " + m.content for m in req.messages]
    )
    prompt = INTERVIEW_REVIEW_PROMPT.format(history=history)
    review = generate(prompt)
    return InterviewEndResponse(review=review.strip())
