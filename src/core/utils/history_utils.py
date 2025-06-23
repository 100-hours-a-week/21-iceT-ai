from typing import List, Dict

MAX_RECENT_MESSAGES = 10
MAX_SUMMARY_MESSAGES = 8

def build_context(messages: List[Dict[str, str]], summary: List[Dict[str, str]] = None) -> List[Dict[str, str]]:
    """
    최근 메시지 10개 + 요약 메시지 최대 8개를 합쳐 LLM 입력용 context 구성

    - messages: 전체 메시지 리스트 (role: user/assistant, content: str)
    - summary: 이전 대화 요약 리스트 (speaker: user/ai, content: str)
    """
    # 최근 메시지 10개 추출
    recent = messages[-MAX_RECENT_MESSAGES:]

    # 요약 메시지는 앞쪽에 삽입 (speaker → role 매핑)
    summary_part = []
    if summary:
        for item in summary:
            if item.get("type") != "chat":
                continue
            role = "user" if item["speaker"] == "user" else "assistant"
            summary_part.append({"role": role, "content": f"[요약] {item['content']}"})
        summary_part = summary_part[-MAX_SUMMARY_MESSAGES:]

    return summary_part + recent
