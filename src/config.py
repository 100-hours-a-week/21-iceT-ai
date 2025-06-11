# src/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ▶️ Upstage 설정
    use_upstage: bool = True
    upstage_model: str = "solar-pro"
    upstage_summary_model: str = "solar-pro2"
    upstage_api_key: str = ""
    upstage_base_url: str = "https://api.upstage.ai/v1"

    # ▶️ Gemini 설정
    use_gemini: bool = True
    gemini_model: str = "gemini-1.5-pro-latest"
    gemini_api_key: str = ""

    # ▶️ vLLM 설정
    vllm_model: str = "Qwen/Qwen2.5-Coder-7B-Instruct"
    vllm_summary_model: str = "qwen1.5-1.8b-chat"
    vllm_url: str = "http://localhost:8001/v1/chat/completions"
    vllm_summary_url: str = "http://localhost:1234/v1/chat/completions"

    # ✅ 공통 LLM 하이퍼파라미터
    sol_temperature: float = 0.3
    sol_max_tokens: int = 8192
    chat_temperature: float = 0.3
    chat_max_tokens: int = 8192
    summary_temperature: float = 0.3
    summary_max_tokens: int = 2048

    # ✅ GCS 및 FAISS 설정
    use_gcs_for_faiss: bool = False
    local_index_dir: str = "vector/faiss_index"
    gcs_bucket: str = ""
    gcs_prefix: str = ""
    vector_store_path: str = "vector/faiss_index"

    # ✅ GCP 인증 키 경로
    google_application_credentials: str = ""

    # ✅ LangSmith 설정
    langsmith_tracing: bool = False
    langsmith_endpoint: str = ""
    langsmith_api_key: str = ""
    langsmith_project: str = ""

    # ✅ 백준 쿠키
    boj_cookie_onlinejudge: str = ""
    boj_cookie_autologin: str = ""

    # ✅ DB 설정
    db_name: str = "koco"
    db_user: str = "user1"
    db_pass: str = "koco"

    # ✅ 백엔드 API 주소
    backend_url: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
