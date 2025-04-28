from fastapi import FastAPI
from src.routers.v1 import solution_router

app = FastAPI(
    title="코딩테스트 도우미 서비스",
    version="1.0.0",
)

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