from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse
from src.adapters.llm_chat import stream_generate
from src.core.prompt_builders import build_interview_followup_prompt, build_interview_review_prompt
from src.schemas.interview_schema import InterviewAnswerRequest, InterviewEndRequest

from src.schemas.interview_schema import (
    InterviewStartRequest, InterviewStartResponse,
    InterviewAnswerRequest, InterviewAnswerResponse,
    InterviewEndRequest, InterviewEndResponse
)
from src.services.interview_service import (
    generate_first_question, generate_followup_question, generate_interview_end
)

router = APIRouter()

#1. 첫 질문
@router.post("/interview/start", response_model=InterviewStartResponse)
async def interview_start(req: InterviewStartRequest):
    result = await generate_first_question(req)
    return InterviewStartResponse(
        sessionId=req.sessionId,
        problemNumber=req.problemNumber,
        title=req.title,
        question=result.question
    )

@router.post("/interview/start-stream")
async def interview_start_stream(req: InterviewStartRequest):
    from src.core.prompt_templates import format_interview_start_prompt

    # 1. 프롬프트 생성
    prompt = format_interview_start_prompt(req.model_dump())

    messages = [
        {"role": "system", "content": "You are a mock technical interviewer. Generate a thoughtful first question."},
        {"role": "user", "content": prompt}
    ]

    # 2. 스트리밍 생성기
    async def event_generator():
        async for token in stream_generate(messages):
            yield {"event": "message", "data": token}

    return EventSourceResponse(event_generator())

# 2. 꼬리 질문
@router.post("/interview/answer", response_model=InterviewAnswerResponse)
async def interview_followup(req: InterviewAnswerRequest):
    return await generate_followup_question(req)

# ⬇️ 이미 있는 라우터 아래에 붙이세요
@router.post("/interview/answer-stream")
async def interview_followup_stream(req: InterviewAnswerRequest):
    prompt = build_interview_followup_prompt(
        messages=req.messages,
        static_summary=req.staticSummary,
        dynamic_summary=req.summary,
        recent_turns=3
    )

    messages = [
        {"role": "system", "content":
            "You are a mock technical interviewer.\n"
            "- Refer to the previous interview summary and recent messages.\n"
            "- Ask only one follow-up question that reflects the user's last answer.\n"
        }
    ]

    async def event_generator():
        async for token in stream_generate(messages):
            yield {"event": "message", "data": token}

    return EventSourceResponse(event_generator())

# 3. 총평
@router.post("/interview/end", response_model=InterviewEndResponse)
async def interview_end(req: InterviewEndRequest):
    return await generate_interview_end(req)

@router.post("/interview/end-stream")
async def interview_end_stream(req: InterviewEndRequest):
    prompt = build_interview_review_prompt(
        messages=req.messages,
        static_summary=req.staticSummary,
        dynamic_summary=req.summary
    )

    messages = [
        {"role": "system", "content":
            "You are a technical interviewer.\n"
            "- Refer to the static problem summary and full interview log provided in the prompt.\n"
            "- Generate a structured JSON review.\n"
        }
    ]

    async def event_generator():
        async for token in stream_generate(messages):
            yield {"event": "message", "data": token}

    return EventSourceResponse(event_generator())
