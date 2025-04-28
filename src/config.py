from pydantic import BaseSettings

class Settings(BaseSettings):
    """
    환경 설정 (환경 변수 기반 로드)
    OPENAI_API_KEY: OpenAI API 키
    MODEL_NAME: 사용할 모델 이름 (MVP: gpt-4o-mini)
    TEMPERATURE: 응답의 창의성 제어 (0~1)
    MAX_TOKENS: 최대 생성 토큰 수
    """
    openai_api_key: str
    model_name: str = "gpt-4o-mini"
    temperature: float = 0.3
    max_tokens: int = 512


settings = Settings() 