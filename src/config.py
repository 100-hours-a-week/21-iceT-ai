# src/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ▶️ Upstage 설정
    use_upstage: bool = True  # True면 Upstage 사용, False면 vLLM 사용

    upstage_model: str = "solar-pro"
    upstage_summary_model: str = "solar-pro2"
    upstage_api_key: str = ""
    upstage_base_url: str = "https://api.upstage.ai/v1"

    # ▶️ Gemini 설정 (solution 전용)
    use_gemini: bool = True
    gemini_model: str = "gemini-1.5-pro-latest"
    gemini_api_key: str = ""

    # ▶️ vLLM 설정
    vllm_model: str = "Qwen/Qwen2.5-Coder-7B-Instruct"
    vllm_summary_model: str = "qwen1.5-1.8b-chat"
    vllm_url: str = "http://localhost:8001/v1/chat/completions"
    vllm_summary_url: str = "http://localhost:1234/v1/chat/completions"

    # ✅ 공통 파라미터
    sol_temperature: float = 0.3
    sol_max_tokens: int = 8192
    chat_temperature: float = 0.3
    chat_max_tokens: int = 8192
    summary_temperature: float = 0.3
    summary_max_tokens: int = 2048

    use_gcs_for_faiss: bool = False
    local_index_dir: str = "vector/faiss_index"
    gcs_bucket: str = ""
    gcs_prefix: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
