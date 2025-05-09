from pydantic_settings import BaseSettings

# 모델 설정
class Settings(BaseSettings):
    model: str = "gpt-4o-mini"
    temperature: float = 0.3
    max_tokens: int = 4096

settings = Settings() 