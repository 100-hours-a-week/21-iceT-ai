from fastapi import FastAPI
from src.core.exception_handlers import (
    validation_exception_handler,
    value_error_handler,
    generic_exception_handler,
    timeout_exception_handler,
)
from src.routers.v1.solution_router import router as solution_router
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI(
    title="코딩테스트 도우미 서비스",
    version="1.0.0",
)

# 예외 핸들러 등록
app.add_exception_handler(ValidationError, validation_exception_handler)
app.add_exception_handler(ValueError, value_error_handler)
app.add_exception_handler(StarletteHTTPException, generic_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)
app.add_exception_handler(TimeoutError, timeout_exception_handler)


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