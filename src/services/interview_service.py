# src/services/interview_service.py

from src.adapters.vllm import generate
from src.schemas.interview_schema import (
    InterviewStartRequest, InterviewStartResponse,
    InterviewAnswerRequest, InterviewAnswerResponse,
    InterviewEndRequest, InterviewEndResponse
)
from src.core.llm_utils import parse_interview_review_response
from src.core.prompt_templates import format_interview_start_prompt

# 1. 첫 질문 생성
async def generate_first_question(req: InterviewStartRequest) -> InterviewStartResponse:
    prompt = format_interview_start_prompt(req.model_dump())

    messages = [
        {"role": "system", "content": "You are a mock technical interviewer. Generate thoughtful questions based on the problem."},
        {"role": "user", "content": prompt}
    ]

    output = await generate(messages)
    return InterviewStartResponse(title=req.title, question=output.strip())

# 2. 꼬리 질문 생성
async def generate_followup_question(req: InterviewAnswerRequest) -> InterviewAnswerResponse:
    chatml_history = [{"role": m.role, "content": m.content} for m in req.messages]

    chatml_history.insert(0, {
        "role": "system",
        "content": "You are a mock technical interviewer. Ask only one follow-up question based on the previous answer."
    })

    output = await generate(chatml_history)
    return InterviewAnswerResponse(session_id=req.session_id, question=output.strip())

# 3. 면접 총평 생성
async def generate_interview_review(req: InterviewEndRequest) -> InterviewEndResponse:
    chatml_history = [{"role": m.role, "content": m.content} for m in req.messages]

    chatml_history.insert(0, {
        "role": "system",
        "content": "You are a technical interviewer. Summarize the interview in the following JSON format only:\n"
                   '{ "good": [...], "bad": [...], "improvement": [...] }'
    })

    raw_output = await generate(chatml_history)
    return parse_interview_review_response(raw_output)
