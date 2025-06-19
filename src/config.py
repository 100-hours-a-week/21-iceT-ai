import platform
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    # 🔐 민감 정보
    gemini_api_key: str
    boj_cookie_onlinejudge: str
    boj_cookie_autologin: str
    db_name: str
    db_user: str
    db_pass: str
    backend_url: str
    service_api_key: str

    # 🔐 Upstage API 키 (최대 20개)
    upstage_key_1: str | None = None
    upstage_key_2: str | None = None
    upstage_key_3: str | None = None
    upstage_key_4: str | None = None
    upstage_key_5: str | None = None
    upstage_key_6: str | None = None
    upstage_key_7: str | None = None
    upstage_key_8: str | None = None
    upstage_key_9: str | None = None
    upstage_key_10: str | None = None

    def get_upstage_keys(self) -> list[str]:
        return [v for i in range(1, 21) if (v := getattr(self, f"upstage_key_{i}", None))]

    @property
    def upstage_key_list(self) -> list[str]:
        return self.get_upstage_keys()

    # ✅ 시스템 기반 경로
    @property
    def local_index_dir(self) -> str:
        system = platform.system().lower()
        if "windows" in system:
            return "C:\\Workspace\\21-iceT-ai\\vector\\faiss_index"
        return "/home/ubuntu/21-iceT-ai/vector/faiss_index"

    # ✅ 모델 분기 기준
    use_vllm: bool = False

    # ✅ 하이퍼파라미터
    sol_temperature: float = 0.3
    sol_max_tokens: int = 8192
    chat_temperature: float = 0.3
    chat_max_tokens: int = 8192
    summary_temperature: float = 0.3
    summary_max_tokens: int = 2048

    # ✅ 모델 이름들
    gemini_model: str = "gemini-2.5-flash"

    upstage_model: str = "solar-pro"
    upstage_summary_model: str = "solar-pro2"
    upstage_base_url: str = "https://api.upstage.ai/v1"

    vllm_model: str = "Qwen/Qwen2.5-Coder-7B-Instruct"
    vllm_summary_model: str = "qwen1.5-1.8b-chat"
    vllm_url: str = "http://localhost:8001/v1/chat/completions"
    vllm_summary_url: str = "http://localhost:1234/v1/chat/completions"

    # ✅ GCP 및 벡터 설정
    google_application_credentials: str = ""
    use_gcs_for_faiss: bool = False
    gcs_bucket: str = ""
    gcs_prefix: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "allow"


settings = Settings()

print("✅ backend_url:", settings.backend_url)