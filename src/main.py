from fastapi import FastAPI
from src.core.logger import setup_logging
from src.core.exception_handlers import add_exception_handlers

# ✅ 기능별 라우터
from src.routers.v1.solution_router import router as solution_router
from src.routers.v2.feedback_router import router as feedback_router
from src.routers.v2.feedback_chat_router import router as feedback_chat_router
from src.routers.v2.interview_router import router as interview_router

# ✅ 로깅 및 예외 핸들러 등록
setup_logging()

app = FastAPI(
    title="코딩테스트 도우미 서비스",
    version="2.0.0",
)

# ✅ 공통 예외 핸들러 등록
add_exception_handlers(app)

# ✅ API 라우터 등록
app.include_router(solution_router,       prefix="/api/v1", tags=["해설 생성"])
app.include_router(feedback_router,       prefix="/api/v2", tags=["코드 피드백"])
app.include_router(feedback_chat_router,  prefix="/api/v2", tags=["피드백 챗봇"])
app.include_router(interview_router,      prefix="/api/v2", tags=["모의 면접"])

# ✅ 헬스체크
@app.get("/healthz")
def healthz():
    return {"status": "ok"}