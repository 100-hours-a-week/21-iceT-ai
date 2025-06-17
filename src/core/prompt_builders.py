from src.core.prompt_templates import (
    format_feedback_chat_prompt,
    format_interview_followup_prompt,
    format_interview_review_prompt
)
from src.schemas.interview_schema import Message

def build_prompt_from_memory(messages: list, summary: str = None, recent_turns: int = 5, mode: str = "feedback") -> str:
    parts = []

    if summary:
        if mode == "feedback":
            parts.append(f"AI: (이전 피드백 요약) {summary.strip()}")
        elif mode == "interview":
            parts.append(f"사용자: 이전 면접 대화 요약을 참고해주세요.\n{summary.strip()}")

    recent_messages = messages[-(recent_turns * 2):]
    for m in recent_messages:
        role = "사용자" if m.role == "user" else "AI"
        parts.append(f"{role}: {m.content}")

    return "\n".join(parts).strip()

def build_feedback_chat_prompt(messages: list[dict],user_input: str,summary: str | None = None,recent_turns: int = 5) -> str:
    parts = []

    if summary:
        parts.append("AI: (이전 피드백 요약)\n" + summary.strip())

    recent = messages[-(recent_turns * 2):]
    for msg in recent:
        prefix = "사용자" if msg["role"] == "user" else "AI"
        parts.append(f"{prefix}: {msg['content']}")

    history_text = "\n".join(parts)
    return format_feedback_chat_prompt(history_text, user_input)



def build_interview_followup_prompt(messages: list[Message], summary: str | None = None, recent_turns: int = 3) -> str:
    parts = []

    if summary:
        parts.append("AI: (이전 대화 요약)\n" + summary.strip())

    recent_messages = messages[-(recent_turns * 2):]
    for msg in recent_messages:
        prefix = "사용자" if msg.role == "user" else "AI"
        parts.append(f"{prefix}: {msg.content}")

    history_text = "\n".join(parts)
    return format_interview_followup_prompt(history_text)


def build_interview_review_prompt(
    messages: list[dict],
    summary: str | None = None
) -> str:
    parts = []

    if summary:
        parts.append("AI: (이전 대화 요약)\n" + summary.strip())

    for msg in messages:
        prefix = "사용자" if msg["role"] == "user" else "AI"
        parts.append(f"{prefix}: {msg['content']}")

    history_text = "\n".join(parts)
    return format_interview_review_prompt(history_text)
