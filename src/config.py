from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    model: str = "gpt-4o-mini"
    temperature: float = 0.3
    max_tokens: int = 4096
    llm_provider: str = "openai"  # "openai" or "vllm"

settings = Settings()
