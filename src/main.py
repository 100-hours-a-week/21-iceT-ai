# 나중에 서버 실행을 위한 메인 함수

from fastapi import FastAPI
from src.core.logger import setup_logging
from src.core.exception_handlers import add_exception_handlers
from src.routers.v1.solution_router import router as solution_router

# 로깅 설정 초기화
setup_logging()

# FastAPI 애플리케이션 생성
app = FastAPI(
    title="코딩테스트 도우미 서비스",
    version="1.0.0",
)

# 예외 핸들러 등록
add_exception_handlers(app)

# API v1 라우터 등록
app.include_router(
    solution_router,
    prefix="/api/ai/v1",
    tags=["해설지 생성 기능"],
)

# health check 엔드포인트
@app.get("/healthz")
def healthz():
    return {"status": "ok"}