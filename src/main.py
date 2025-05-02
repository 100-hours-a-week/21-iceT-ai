from fastapi import FastAPI
from src.core.logger import setup_logging
from src.core.exception_handlers import add_exception_handlers
from src.routers.v1.solution_router import router as solution_router

setup_logging()

app = FastAPI(
    title="코딩테스트 도우미 서비스",
    version="1.0.0",
)

# 예외 핸들러 등록
add_exception_handlers(app)

# API v1 라우터 등록
app.include_router(
    solution_router,
    prefix="/api/v1",
    tags=["해설지 생성 기능"],
)

# health check
@app.get("/healthz")
def healthz():
    return {"status": "ok"} 