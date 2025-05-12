import re
import json

from src.schemas.feedback_schema import FeedbackResponse
from src.schemas.solution_schema import SolutionResponse
from src.schemas.interview_schema import InterviewEndResponse, InterviewReview


def parse_json_from_llm_output(raw_output: str) -> dict:
    """```json 마크다운 제거 후 JSON 파싱"""
    cleaned = re.sub(r"^```json\s*|\s*```$", "", raw_output.strip())
    return json.loads(cleaned)


def parse_feedback_response(raw_output: str, title: str) -> FeedbackResponse:
    try:
        parsed = parse_json_from_llm_output(raw_output)
        return FeedbackResponse(
            title=title,
            good=parsed["good"],
            bad=parsed["bad"],
            improved_code=parsed["improved_code"]
        )
    except Exception as e:
        raise ValueError(f"❌ LLM 응답 파싱 실패: {e}\n\n[출력 원문]:\n{raw_output}")


def parse_solution_response(raw_output: str) -> SolutionResponse:
    try:
        parsed = parse_json_from_llm_output(raw_output)
        return SolutionResponse(**parsed)
    except Exception as e:
        raise ValueError(f"❌ Qwen 응답을 JSON으로 파싱하지 못했습니다.\n\n[원본 응답]:\n{raw_output}\n\n[에러]: {e}")


def parse_interview_review_response(raw_output: str) -> InterviewEndResponse:
    try:
        parsed = parse_json_from_llm_output(raw_output)
        return InterviewEndResponse(review=InterviewReview(**parsed))
    except Exception as e:
        raise ValueError(f"총평 JSON 파싱 실패: {e}\n출력:\n{raw_output}")
