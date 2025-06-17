from src.schemas.summary_schema import SummaryRequest, SummaryResponse
from src.adapters.llm_summary import generate_summary as call_llm_summary

def get_summary_prompt(mode: str) -> str:
    if mode == "feedback":
        return """아래는 코드 리뷰에 대한 사용자와 AI의 대화입니다.
질문에 대한 답변 흐름을 간결하게 요약하고, 중요한 피드백 흐름을 잊지 않도록 정리하세요.

응답은 다음 JSON 형식으로만 출력하세요:

{
  "summary": "요약 내용. 예: 사용자는 코드 개선 방향에 대해 질문했고, AI는 시간 복잡도와 정렬 기반 대안을 제안함"
}

※ 마크다운, 문장, 설명 없이 JSON만 출력하세요.
"""
    elif mode == "interview":
        return """아래는 코딩 테스트 기반 모의 면접 대화입니다.
질문과 답변의 흐름을 유지하며 핵심 포인트만 요약하세요.

응답은 다음 JSON 형식으로만 출력하세요:

{
  "summary": "요약 내용. 예: 첫 질문은 시간 복잡도에 대한 것이었고, 사용자는 O(n)이라 답함. 이후 입력 검증에 대한 질문이 이어짐."
}

※ 마크다운, 문장, 설명 없이 JSON만 출력하세요.
"""
    else:
        raise ValueError(f"알 수 없는 mode: {mode}")

async def generate_summary(req: SummaryRequest) -> SummaryResponse:
    messages = [{"role": m.role, "content": m.content} for m in req.messages]
    
    messages.insert(0, {
        "role": "system",
        "content": get_summary_prompt(req.mode)
    })

    summary = await call_llm_summary(messages)

    return SummaryResponse(
        sessionId=req.sessionId,
        summary=summary.strip()
    )