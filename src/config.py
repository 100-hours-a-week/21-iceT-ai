from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    model: str = "Qwen/Qwen2.5-Coder-7B-Instruct"
    temperature: float = 0.3
    max_tokens: int = 4096

settings = Settings()
