import uvicorn
from fastapi import FastAPI
from src.core.logger import setup_logging
from src.core.exception_handlers import add_exception_handlers
from src.routers.router import router

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

# 모든 엔드포인트는 router.py에서 관리
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)