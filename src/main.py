import uvicorn, os
from fastapi import FastAPI
from src.core.logger import setup_logging
from src.core.exception_handlers import add_exception_handlers
from src.routers.v1.solution_router import router as solution_router
from src.routers.v2 import summary_router, feedback_router, interview_router

def clear_csv_logs():
    base_path = "tests/DB"
    files_to_clear = {
        "chat_record.csv": ["sessionId", "turn", "role", "content", "createdAt"],
        "chat_session.csv": ["sessionId", "problemNumber", "title", "createdAt"],
        "chat_summary.csv": ["sessionId", "turn", "summary", "createdAt"],
    }

    os.makedirs(base_path, exist_ok=True)

    for filename, header in files_to_clear.items():
        filepath = os.path.join(base_path, filename)
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            import csv
            writer = csv.writer(f)
            writer.writerow(header)
        print(f"[INIT] 초기화 완료: {filepath}")


setup_logging()
clear_csv_logs()

app = FastAPI(
    title="코딩테스트 도우미 서비스",
    version="1.0.0"
)

add_exception_handlers(app)

# health check 엔드포인트
@app.get("/healthz")
def healthz():
    return {"status": "ok"}

# API v1 라우터 등록
app.include_router(
    solution_router,
    prefix="/api/ai/v1",
    tags=["해설지 생성 기능"]
)

# API v2 라우터 등록
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