from fastapi import FastAPI
from src.routers.v1 import SolutionRouter

app = FastAPI(
    title="한영 코딩테스트 해설 서비스",
    version="1.0.0",
)

# API v1 라우터 등록
app.include_router(
    SolutionRouter,
    prefix="/api/v1",
    tags=["해설"],
)

# health check
@app.get("/healthz")
def healthz():
    return {"status": "ok"}