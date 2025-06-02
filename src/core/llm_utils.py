import re
import json
from typing import List

# 피드백
from src.schemas.feedback_schema import (
    FeedbackResponse,
    FeedbackAnswerResponse
)

# 면접
from src.schemas.interview_schema import (
    InterviewStartRequest,
    InterviewStartResponse,
    InterviewAnswerResponse,
    InterviewEndResponse,
)

# 문제 풀이
from src.schemas.solution_schema import SolutionResponse

# 요약
from src.schemas.summary_schema import SummaryResponse

def parse_json_from_llm_output(raw_output: str) -> dict:
    """LLM 출력에서 마크다운 제거 및 JSON 파싱 (이중 파싱 포함)"""
    print("✅ [DEBUG] 파싱 대상 원문:\n", raw_output)

    cleaned = re.sub(r"^```json\s*|\s*```$", "", raw_output.strip())

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        print("⚠️ 1st parse failed:", e)
        try:
            return json.loads(json.loads(cleaned))
        except Exception as e2:
            print("❌ double json.loads failed:", e2)
            raise

def validate_keys(parsed: dict, required_keys: List[str]):
    for key in required_keys:
        if key not in parsed:
            raise ValueError(f"필수 키 누락: '{key}'")

#솔루션
def parse_solution_response(raw_output: str) -> SolutionResponse:
    parsed = parse_json_from_llm_output(raw_output)
    validate_keys(parsed, ["problemNumber", "problemCheck", "problemSolving", "solutionCode"])
    validate_keys(parsed["problemCheck"], ["problemDescription", "algorithm"])
    validate_keys(parsed["solutionCode"], ["python", "cpp", "java"])
    return SolutionResponse(**parsed)

#피드백
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

#인터뷰
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

def parse_summary_response(raw_output: str, session_id: str) -> SummaryResponse:
    parsed = parse_json_from_llm_output(raw_output)
    validate_keys(parsed, ["summary"])
    return SummaryResponse(sessionId=session_id, summary=parsed["summary"])

def build_prompt_from_memory(messages: list, summary: str = None, recent_turns: int = 3) -> str:
    prompt_parts = []

    if summary:
        prompt_parts.append(f"📝 요약:\n{summary.strip()}\n")

    recent_messages = messages[-(recent_turns * 2):]
    for m in recent_messages:
        role = "사용자" if m.role == "user" else "AI"
        prompt_parts.append(f"{role}: {m.content}")

    return "\n".join(prompt_parts).strip()
