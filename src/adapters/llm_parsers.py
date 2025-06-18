import re
import json
from typing import List

# 응답 스키마
from src.schemas.feedback_schema import FeedbackResponse, FeedbackAnswerResponse
from src.schemas.interview_schema import (
    InterviewStartRequest, InterviewStartResponse,
    InterviewAnswerResponse, InterviewEnd, InterviewEndResponse
)
from src.schemas.solution_schema import SolutionResponse
from src.schemas.summary_schema import TurnSummaryResponse


# ✅ 공통 유틸
def parse_json_from_llm_output(raw_output: str) -> dict:
    """LLM 출력에서 마크다운 제거 및 JSON 파싱 (이중 파싱 포함)"""
    cleaned = re.sub(r"^```json\s*|\s*```$", "", raw_output.strip())
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return json.loads(json.loads(cleaned))  # nested JSON 대응

def validate_keys(parsed: dict, required_keys: List[str]):
    for key in required_keys:
        if key not in parsed:
            raise ValueError(f"필수 키 누락: '{key}'")


# ✅ 피드백 응답
def parse_feedback_response(raw_output: str, data: dict) -> FeedbackResponse:
    parsed = parse_json_from_llm_output(raw_output)
    validate_keys(parsed, ["good", "bad", "improved_code"])
    return FeedbackResponse(
        sessionId=data.get("sessionId", ""),
        problemNumber=data.get("problemNumber", 0),
        title=data.get("title", "제목 없음"),
        good=parsed["good"],
        bad=parsed["bad"],
        improvedCode=parsed["improved_code"]
    )

def parse_feedback_answer_response(raw_output: str, session_id: str) -> FeedbackAnswerResponse:
    parsed = parse_json_from_llm_output(raw_output)
    validate_keys(parsed, ["answer"])
    return FeedbackAnswerResponse(sessionId=session_id, answer=parsed["answer"])


# ✅ 인터뷰 응답
def parse_interview_start_response(raw_output: str, req: InterviewStartRequest) -> InterviewStartResponse:
    parsed = parse_json_from_llm_output(raw_output)
    validate_keys(parsed, ["question"])
    return InterviewStartResponse(
        sessionId=req.sessionId,
        problemNumber=req.problemNumber,
        title=req.title,
        question=parsed["question"]
    )

def parse_interview_answer_response(raw_output: str, session_id: str) -> InterviewAnswerResponse:
    parsed = parse_json_from_llm_output(raw_output)
    validate_keys(parsed, ["question"])
    return InterviewAnswerResponse(sessionId=session_id, question=parsed["question"])

def parse_interview_end_response(raw_output: str) -> InterviewEndResponse:
    parsed = parse_json_from_llm_output(raw_output)
    validate_keys(parsed, ["good", "bad", "improvement"])
    return InterviewEndResponse(review=InterviewEnd(**parsed))


# ✅ 솔루션 응답
def parse_solution_response(raw_output: str) -> SolutionResponse:
    parsed = parse_json_from_llm_output(raw_output)
    validate_keys(parsed, ["problemNumber", "problemCheck", "problemSolving", "solutionCode"])
    validate_keys(parsed["problemCheck"], ["problemDescription", "algorithm"])
    validate_keys(parsed["solutionCode"], ["python", "cpp", "java"])
    return SolutionResponse(**parsed)


# ✅ 요약 응답
def parse_summary_response(raw_output: str, session_id: str) -> TurnSummaryResponse:
    parsed = parse_json_from_llm_output(raw_output)
    validate_keys(parsed, ["summary"])
    return TurnSummaryResponse(sessionId=session_id, summary=parsed["summary"])


# ✅ 파서 레지스트리
SCHEMA_PARSERS = {
    FeedbackResponse: parse_feedback_response,
    FeedbackAnswerResponse: parse_feedback_answer_response,
    InterviewStartResponse: parse_interview_start_response,
    InterviewAnswerResponse: parse_interview_answer_response,
    InterviewEndResponse: parse_interview_end_response,
    SolutionResponse: parse_solution_response,
    TurnSummaryResponse: parse_summary_response,
}
