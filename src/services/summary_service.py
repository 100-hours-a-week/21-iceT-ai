from src.schemas.chat_schema import SummaryRequest, SummaryResponse
from src.adapters.llm_summary import generate_summary_from_cpu_model  # ✅ 3단계에서 만들 예정

def get_summary_prompt(mode: str) -> str:
    if mode == "feedback":
        return """아래 코드 리뷰 대화를 요약하세요. 핵심 피드백 흐름을 정리하세요.

응답은 반드시 다음과 같은 JSON 형식으로 출력하세요:

{
  "summary": "대화 요약 내용"
}

추가 설명, 마크다운, 문장 등은 포함하지 마세요. 정확한 JSON만 출력하세요.
"""
    elif mode == "interview":
        return """아래 면접 대화를 요약하세요. 질문과 답변의 흐름을 간결하게 정리하세요.

응답은 반드시 다음과 같은 JSON 형식으로 출력하세요:

{
  "summary": "대화 요약 내용"
}

추가 설명, 마크다운, 문장 등은 포함하지 마세요. 정확한 JSON만 출력하세요.
"""
    else:
        raise ValueError(f"알 수 없는 mode: {mode}")

async def generate_summary(req: SummaryRequest) -> SummaryResponse:
    # ChatML history 구성
    messages = [{"role": m.role, "content": m.content} for m in req.messages]
    messages.insert(0, {
        "role": "system",
        "content": get_summary_prompt(req.mode)
    })

    # CPU용 요약 모델 호출
    summary = await generate_summary_from_cpu_model(messages)

    return SummaryResponse(
        sessionId=req.sessionId,
        summary=summary.strip()
    )
