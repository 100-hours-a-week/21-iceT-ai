import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    model_solution: str = "gemini-2.5-flash"
    temperature_solution: float = 0.3
    max_tokens_solution: int = 8192

    model_chat: str = "solar-pro"
    temperature_chat: float = 0.3
    
    max_tokens_feedback_start: int = 4096
    max_tokens_feedback_answer: int = 1024
    max_tokens_interview_start: int = 768
    max_tokens_interview_answer: int = 1024
    max_tokens_summary: int = 768

    model_config = {"protected_namespaces": ("settings_",)}

settings = Settings() 

BACKEND_URL     = os.getenv("BACKEND_URL")
BACKEND_TIMEOUT = float(os.getenv("BACKEND_TIMEOUT", "10.0"))
