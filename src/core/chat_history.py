from typing import List, Dict, Optional
from src.config import settings

def build_context_text(messages: List[Dict[str, str]], summary: Optional[str] = None) -> str:
    recent = messages[-settings.max_recent_messages:]

    summary_part = []
    if summary:
        summary_part.append({
            "role": "system",
            "content": f"[요약된 문제 및 대화 정보]\n{summary.strip()}"
        })
    # 중요도 계산: 최신 메시지일수록 중요도 높음
    n = len(recent)
    weighted_msgs = []
    for i, m in enumerate(recent):
        # 최신 메시지일수록 중요도 1.0, 그 다음 0.9, ... (선형 감소)
        weight = round(1.0 - 0.1 * (n - i - 1), 2)
        weighted_msgs.append({
            "role": m["role"],
            "content": f"[중요도: {weight}] {m['content']}"
        })
    full_context = summary_part + weighted_msgs
    return "\n".join(f"{m['role']}: {m['content']}" for m in full_context)