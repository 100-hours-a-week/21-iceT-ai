import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

# 모델 설정
# class Settings(BaseSettings):
#     model: str = "gpt-4.1-mini"
#     temperature: float = 0.3
#     max_tokens: int = 8192

# Gemini 모델 설정
class Settings(BaseSettings):
    # model: str = "gemini-2.0-flash"
    model: str = "gemini-2.5-flash-preview-05-20"
    temperature: float = 0.3
    max_tokens: int = 8192

settings = Settings() 

# 백앤드 설정
BACKEND_URL     = os.getenv("BACKEND_URL")
BACKEND_TIMEOUT = float(os.getenv("BACKEND_TIMEOUT", "10.0"))

# 서비스 설정
SERVICE_API_KEY = os.getenv("SERVICE_API_KEY")