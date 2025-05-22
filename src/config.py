from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model: str = "Qwen/Qwen2.5-Coder-7B-Instruct"
    vllm_url: str = "http://localhost:8001/v1/chat/completions"
    temperature: float = 0.3
    max_tokens: int = 4096

    class Config:
        env_file = ".env"  # ✅ .env 파일 자동 로드


settings = Settings()
print("✅ [CONFIG] Loaded vllm_url:", settings.vllm_url)