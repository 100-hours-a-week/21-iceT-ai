from src.config import settings

if settings.llm_provider != "openai":
    raise ImportError("llm_client는 OpenAI 환경에서만 사용해야 합니다.")

from src.adapters.llm_client_base import llm, generate_solution
