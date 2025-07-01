import uvicorn
from fastapi import FastAPI
from src.core.logger import setup_logging
from src.core.exception_handlers import add_exception_handlers
from src.routers.v1.solution_router import router as solution_router
from src.routers.v2 import solution_router_v2, feedback_router, interview_router, summary_router

# 로깅 설정 초기화
setup_logging()

# FastAPI 애플리케이션 생성
app = FastAPI(
    title="코딩테스트 도우미 서비스",
    version="1.0.0",
)

# 예외 핸들러 등록
add_exception_handlers(app)

# health check 엔드포인트
@app.get("/healthz")
def healthz():
    return {"status": "ok"}

# API v1 라우터 등록
app.include_router(
    solution_router,
    prefix="/api/ai/v1",
    tags=["해설지 생성 기능"],
)

# API v2 라우터 등록
app.include_router(
    solution_router_v2.router,
    prefix="/api/ai/v2",
    tags=["해설지 생성 기능 v2"],
)

app.include_router(
    summary_router.router,
    prefix="/api/ai/v2",
    tags=["대화 요약 기능"]
)

app.include_router(
    feedback_router.router,
    prefix="/api/ai/v2",
    tags=["피드백 기능"]
)

app.include_router(
    interview_router.router,
    prefix="/api/ai/v2",
    tags=["인터뷰 기능"]
)

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)