from typing import List, Dict, Optional
from src.chatbot.config import settings

def build_context_text(messages: List[Dict[str, str]], summary: Optional[str] = None) -> str:
    recent = messages[-settings.max_recent_messages:]

    summary_part = []
    if summary:
        summary_part.append({
            "role": "system",
            "content": f"[요약된 문제 및 대화 정보]\n{summary.strip()}"
        })

    full_context = summary_part + recent
    return "\n".join(f"{m['role']}: {m['content']}" for m in full_context)