from fastapi import FastAPI
from src.core.logger import setup_logging
from src.core.exception_handlers import add_exception_handlers

# ✅ 기능별 라우터
from src.routers.v1.solution_router import router as solution_router  # 해설 기능
from src.routers.v2.feedback_router import router as feedback_router  # 코드 피드백 챗봇
from src.routers.v2.interview_router import router as interview_router  # 모의 면접 챗봇

# ✅ 로그 및 예외 설정
setup_logging()

app = FastAPI(
    title="코딩테스트 도우미 서비스",
    version="2.0.0",
)

# ✅ 공통 예외 핸들러 등록
add_exception_handlers(app)

# ✅ 라우터 등록
app.include_router(solution_router, prefix="/api/v1", tags=["해설지 생성 기능"])
app.include_router(feedback_router, prefix="/api/v2", tags=["코드 피드백 챗봇"])
app.include_router(interview_router, prefix="/api/v2", tags=["모의 면접 챗봇"])

# ✅ 헬스체크
@app.get("/healthz")
def healthz():
    return {"status": "ok"}
