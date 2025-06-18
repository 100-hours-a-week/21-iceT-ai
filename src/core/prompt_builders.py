from src.core.prompt_templates import (
    format_feedback_chat_prompt,
    format_interview_followup_prompt,
    format_interview_review_prompt
)
from src.schemas.interview_schema import Message

def flatten_structured_summary(summary_list: list[dict]) -> str:
    return "\n".join(
        f'{s["speaker"]}: ({s.get("intent", "요약")}) {s["content"]}'
        for s in summary_list
    )

def build_prompt_from_memory(
    messages: list,
    static_summary: str | list[dict] | None = None,
    dynamic_summary: str | list[dict] | None = None,
    recent_turns: int = 5,
    mode: str = "feedback"
) -> str:
    parts = []

    def flatten(s):  # 공통 flatten 함수
        if isinstance(s, list):
            return flatten_structured_summary(s)
        elif isinstance(s, str):
            return s.strip()
        return ""

    #  1. static summary 먼저 삽입
    if static_summary:
        parts.append(f"📌 문제 정보 요약\n{flatten(static_summary)}")

    #  2. dynamic summary 다음 삽입
    if dynamic_summary:
        if mode == "feedback":
            parts.append(f"AI: (이전 피드백 요약)\n{flatten(dynamic_summary)}")
        elif mode == "interview":
            parts.append(f"사용자: 이전 면접 대화 요약 참고\n{flatten(dynamic_summary)}")

    #  3. 최근 메시지 turn 삽입
    for m in messages[-(recent_turns * 2):]:
        role = "사용자" if m.role == "user" else "AI"
        parts.append(f"{role}: {m.content}")

    return "\n".join(parts).strip()


def build_feedback_chat_prompt(
    messages: list[dict],
    user_input: str,
    summary: str | list[dict] | None = None,
    recent_turns: int = 5
) -> str:
    parts = []

    # 요약 삽입
    if summary:
        if isinstance(summary, list):
            parts.append("AI: (이전 피드백 요약)\n" + flatten_structured_summary(summary))
        else:
            parts.append("AI: (이전 피드백 요약)\n" + summary.strip())

    # 최근 대화 turn 삽입
    recent = messages[-(recent_turns * 2):]
    for msg in recent:
        prefix = "사용자" if msg["role"] == "user" else "AI"
        parts.append(f"{prefix}: {msg['content']}")

    history_text = "\n".join(parts)
    return format_feedback_chat_prompt(history_text, user_input)


def build_interview_followup_prompt(
    messages: list[Message],
    static_summary: str | list[dict] | None = None,
    dynamic_summary: str | list[dict] | None = None,
    recent_turns: int = 3
) -> str:
    parts = []

    def flatten(s):
        if isinstance(s, list):
            return flatten_structured_summary(s)
        elif isinstance(s, str):
            return s.strip()
        return ""

    # ✅ 문제 정보 요약 먼저
    if static_summary:
        parts.append("📌 문제 정보 요약\n" + flatten(static_summary))

    # ✅ 이전 대화 요약
    if dynamic_summary:
        parts.append("이전 면접 요약:\n" + flatten(dynamic_summary))

    # ✅ 최근 메시지
    for msg in messages[-(recent_turns * 2):]:
        prefix = "사용자" if msg.role == "user" else "AI"
        parts.append(f"{prefix}: {msg.content}")

    return format_interview_followup_prompt("\n".join(parts))


def build_interview_review_prompt(
    messages: list[dict],
    static_summary: str | list[dict] | None = None,
    dynamic_summary: str | list[dict] | None = None
) -> str:
    parts = []

    def flatten(s):
        if isinstance(s, list):
            return flatten_structured_summary(s)
        elif isinstance(s, str):
            return s.strip()
        return ""

    if static_summary:
        parts.append("📌 문제 정보 요약\n" + flatten(static_summary))

    if dynamic_summary:
        parts.append("이전 면접 요약:\n" + flatten(dynamic_summary))

    for msg in messages:
        prefix = "사용자" if msg["role"] == "user" else "AI"
        parts.append(f"{prefix}: {msg['content']}")

    return format_interview_review_prompt("\n".join(parts))

