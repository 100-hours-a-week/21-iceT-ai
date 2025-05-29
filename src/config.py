# src/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ✅ vLLM 메인 모델 설정
    vllm_model: str = "Qwen/Qwen2.5-Coder-7B-Instruct"
    vllm_url: str = "http://localhost:8001/v1/chat/completions"
    generation_temperature: float = 0.3
    generation_max_tokens: int = 4096

    # ✅ 요약용 LLM 설정 (보통 CPU 기반 Qwen 1.8B)
    summary_model: str = "qwen1.5-1.8b-chat"
    summary_llm_url: str = "http://localhost:1234/v1/chat/completions"
    summary_temperature: float = 0.3
    summary_max_tokens: int = 512

    # ✅ Gemini 설정
    use_gemini: bool = False
    gemini_model: str = "gemini-pro"
    gemini_api_key: str = ""

    # ✅ Upstage 설정
    use_upstage: bool = True
    model: str = "solar-pro-250422"
    upstage_api_key: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
