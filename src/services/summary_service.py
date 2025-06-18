from src.config import settings
from src.schemas.summary_schema import SummaryRequest, TurnSummaryResponse
from src.adapters.llm_summary import generate_summary_from_upstage, generate_summary_from_vllm

def get_summary_prompt(mode: str) -> str:
    if mode == "feedback":
        return """아래는 사용자와 AI가 나눈 코드 리뷰 대화입니다.
각 발화를 요약하여 다음 JSON 배열 형식으로 출력하세요:

[
  {"speaker": "user", "intent": "질문", "content": "이 코드가 입력이 많을 때도 괜찮을까요?"},
  {"speaker": "ai", "intent": "성능 분석", "content": "O(n^2) 복잡도는 대규모 입력에서 느릴 수 있어요. 정렬 기반으로 개선하세요."}
]

📌 출력 규칙:
- 각 항목은 정확히 `speaker`, `intent`, `content` 3개 필드를 포함해야 합니다.
- `speaker`는 "user" 또는 "ai" 중 하나
- `intent`는 질문, 설명, 반론, 조언, 인정 등 1~2단어
- `content`는 핵심만 요약한 한 문장 (권장: 50자 이내)
- 절대 마크다운, 설명, 코드 없이 JSON 배열만 출력하세요
"""
    elif mode == "interview":
        return """아래는 사용자와 AI 간의 코딩 인터뷰 대화입니다.
각 발화를 요약하여 다음 JSON 배열로 출력하세요:

[
  {"speaker": "user", "intent": "답변", "content": "이중 반복문으로 O(n^2)이고, 입력이 작으니 괜찮다고 판단했습니다."},
  {"speaker": "ai", "intent": "후속 질문", "content": "입력 범위가 커지면 이 코드가 어떤 문제가 있을까요?"}
]

📌 출력 규칙:
- 각 항목은 `{ "speaker": ..., "intent": ..., "content": ... }` 형식
- `speaker`: "user" 또는 "ai"
- `intent`: 답변, 질문, 설명, 유도, 반론 등 명확한 목적을 단어로 표현
- `content`: 해당 발화의 요지를 1문장으로 요약 (가능하면 50자 내외)
- JSON 배열만 출력 (마크다운, 설명, 문장 절대 금지)
"""

    else:
        raise ValueError(f"알 수 없는 mode: {mode}")

async def generate_summary(req: SummaryRequest) -> TurnSummaryResponse:
    messages = [{"role": m.role, "content": m.content} for m in req.messages[-20:]]

    if settings.use_upstage:
        return await generate_summary_from_upstage(messages, req.sessionId)
    else:
        return await generate_summary_from_vllm(messages, req.sessionId)
