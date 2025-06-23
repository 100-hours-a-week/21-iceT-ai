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
    max_tokens_chat: int = 8192

    model_config = {"protected_namespaces": ("settings_",)}

settings = Settings() 

BACKEND_URL     = os.getenv("BACKEND_URL")
BACKEND_TIMEOUT = float(os.getenv("BACKEND_TIMEOUT", "10.0"))
