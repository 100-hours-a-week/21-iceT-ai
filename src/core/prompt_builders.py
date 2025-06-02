def build_prompt_from_memory(messages: list, summary: str = None, recent_turns: int = 3, mode: str = "feedback") -> str:
    prompt_parts = []

    if summary:
        if mode == "feedback":
            prompt_parts.append(f"AI: (이전 피드백 요약) {summary.strip()}")
        elif mode == "interview":
            prompt_parts.append(f"사용자: 이전 면접 대화 요약을 참고해주세요.\n{summary.strip()}")

    recent_messages = messages[-(recent_turns * 2):]
    for m in recent_messages:
        role = "사용자" if m.role == "user" else "AI"
        prompt_parts.append(f"{role}: {m.content}")

    return "\n".join(prompt_parts).strip()
