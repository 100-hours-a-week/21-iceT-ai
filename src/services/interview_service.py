from src.adapters.llm_chat import generate
from src.schemas.interview_schema import (
    InterviewStartRequest, InterviewStartResponse,
    InterviewAnswerRequest, InterviewAnswerResponse,
    InterviewEndRequest, InterviewEndResponse, InterviewEnd
)
from src.core.prompt_templates import format_interview_start_prompt, format_interview_followup_prompt, format_interview_review_prompt  
from src.core.prompt_builders import build_interview_followup_prompt, build_interview_review_prompt
from src.config import settings
import json

# 1. 첫 질문 생성
async def generate_first_question(req: InterviewStartRequest) -> InterviewStartResponse:
    prompt = format_interview_start_prompt(req.model_dump())

    messages = [
        {"role": "system", "content": "You are a mock technical interviewer. Generate thoughtful questions based on the problem."},
        {"role": "user", "content": prompt}
    ]

    if settings.use_upstage:
        return await generate(messages, schema_class=InterviewStartResponse)
    else:
        raw_output = await generate(messages)
        parsed = json.loads(raw_output.strip().strip("```json").strip("```"))
        return InterviewStartResponse(
            sessionId=req.sessionId,
            problemNumber=req.problemNumber,
            title=req.title,
            question=parsed["question"]
        )

# 2. 꼬리 질문 생성
async def generate_followup_question(req: InterviewAnswerRequest) -> InterviewAnswerResponse:
    prompt = build_interview_followup_prompt(req.messages, req.summary, recent_turns=3)
    messages = [
        {"role": "system", "content": "You are a mock technical interviewer. Ask only one follow-up question."},
        {"role": "user", "content": prompt}
    ]

    if settings.use_upstage:
        return await generate(messages, schema_class=InterviewAnswerResponse)
    else:
        raw_output = await generate(messages)
        parsed = json.loads(raw_output.strip().strip("```json").strip("```"))
        return InterviewAnswerResponse(
            sessionId=req.sessionId,
            question=parsed["question"]
        )

# 3. 면접 총평 생성
async def generate_interview_end(req: InterviewEndRequest) -> InterviewEndResponse:
    prompt = build_interview_review_prompt(req.messages, req.summary)

    messages = [
        {"role": "system", "content": "You are a technical interviewer."},
        {"role": "user", "content": prompt}
    ]

    if settings.use_upstage:
        return await generate(messages, schema_class=InterviewEndResponse)
    else:
        raw_output = await generate(messages)
        parsed = json.loads(raw_output.strip().strip("```json").strip("```"))
        return InterviewEndResponse(review=InterviewEnd(**parsed))

