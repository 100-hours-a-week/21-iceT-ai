import re
import json

from src.schemas.feedback_schema import FeedbackResponse
from src.schemas.solution_schema import SolutionResponse
from src.schemas.interview_schema import InterviewEndResponse, InterviewReview


import json
import re
from src.schemas.feedback_schema import FeedbackResponse

def parse_json_from_llm_output(raw_output: str) -> dict:
    """LLM 출력에서 마크다운 제거 및 JSON 파싱 (이중 파싱 포함)"""
    cleaned = re.sub(r"^```json\s*|\s*```$", "", raw_output.strip())

    try:
        parsed = json.loads(cleaned)
        return parsed
    except json.JSONDecodeError as e:
        print("⚠️ 1st parse failed:", e)
        try:
            parsed = json.loads(json.loads(cleaned))
            print("✅ [DEBUG] double-parsed:", parsed)
            return parsed
        except Exception as e2:
            print("❌ double json.loads failed:", e2)
            raise


def parse_feedback_response(raw_output: str, title: str) -> FeedbackResponse:
    print("🧾 LLM 응답 원문:\n" + "-" * 50)
    print(raw_output)
    print("-" * 50)

    try:
        parsed = parse_json_from_llm_output(raw_output)

        # ✅ 구조 검증
        if not isinstance(parsed, dict):
            raise ValueError("파싱된 결과가 dict가 아닙니다.")
        for key in ("good", "bad", "improved_code"):
            if key not in parsed:
                raise ValueError(f"예상 키 누락: '{key}'")

        return FeedbackResponse(
            title=title,
            good=parsed["good"],
            bad=parsed["bad"],
            improved_code=parsed["improved_code"]
        )

    except Exception as e:
        print("❌ parse_feedback_response 실패:", e)
        # ✅ fallback 응답 반환 (서버 죽지 않게)
        return FeedbackResponse(
            title=title or "피드백 생성 실패",
            good=[],
            bad=[f"⚠️ 오류: {str(e)}"],
            improved_code="⚠️ 파싱 실패: 모델 응답이 올바른 JSON 형식이 아닙니다."
        )


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
