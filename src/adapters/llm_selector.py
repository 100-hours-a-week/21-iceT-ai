from src.config import settings
import importlib

if settings.llm_provider == "vllm":
    m = importlib.import_module("src.adapters.vllm")
elif settings.llm_provider == "openai":
    m = importlib.import_module("src.adapters.llm_client")
else:
    raise ImportError("지원되지 않는 LLM_PROVIDER 설정")

generate_solution = m.generate_solution
llm = m.llm

__all__ = ["generate_solution", "llm"]
