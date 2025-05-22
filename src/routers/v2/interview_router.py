from fastapi import APIRouter
from uuid import uuid4  # ✅ 추가

from src.schemas.interview_schema import (
    InterviewStartRequest, InterviewStartResponse,
    InterviewAnswerRequest, InterviewAnswerResponse,
    InterviewEndRequest, InterviewEndResponse
)
from src.services.interview_service import (
    generate_first_question, generate_followup_question, generate_interview_review
)

router = APIRouter()

#1. 첫 질문
@router.post("/interview/start", response_model=InterviewStartResponse)
async def interview_start(req: InterviewStartRequest):
    session_id = str(uuid4())
    result = await generate_first_question(req)
    return InterviewStartResponse(
        sessionId=session_id,
        problemNumber=req.problemNumber,
        title=req.title,
        question=result.question
    )

# 2. 꼬리 질문
@router.post("/interview/answer", response_model=InterviewAnswerResponse)
async def interview_followup(req: InterviewAnswerRequest):
    return await generate_followup_question(req)

# 3. 총평
@router.post("/interview/end", response_model=InterviewEndResponse)
async def interview_end(req: InterviewEndRequest):
    return await generate_interview_review(req)