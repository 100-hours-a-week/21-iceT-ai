# src/main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import ValidationError
from logging.handlers import RotatingFileHandler

import logging
import uvicorn
import os

from src.routers.solution_router import router as solution_router
from src.routers.feedback_router import router as feedback_router
from src.routers.interview_router import router as interview_router
from src.routers.summary_router import router as summary_router

app = FastAPI()

# ✅ Logging setup
LOG_DIR = os.getenv("LOG_DIR", "logs")
os.makedirs(LOG_DIR, exist_ok=True)
fmt = "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=fmt,
    handlers=[
        logging.StreamHandler(),
        RotatingFileHandler(
            filename=os.path.join(LOG_DIR, "app.log"),
            maxBytes=10*1024*1024,
            backupCount=5,
            encoding="utf-8",
        )
    ],
)

# ✅ Exception handlers
def format_error_response(code: str, message: str, hint: str = ""):
    return {"error": {"code": code, "message": message, "hint": hint}}

@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    logging.warning(f"[RequestValidationError] {exc}")
    return JSONResponse(
        status_code=422,
        content=format_error_response("REQUEST_VALIDATION_FAILED", "요청 JSON 구조가 잘못되었습니다.", str(exc))
    )

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    logging.warning(f"[ValidationError] {exc}")
    return JSONResponse(
        status_code=400,
        content=format_error_response("INVALID_REQUEST", "입력 형식이 잘못되었습니다.", str(exc))
    )

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    logging.error(f"[ValueError] {exc}")
    return JSONResponse(
        status_code=422,
        content=format_error_response("LLM_PARSE_FAILED", "모델의 응답을 처리하는 중 오류가 발생했습니다.", str(exc))
    )

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logging.error(f"[HTTPException] {exc.status_code} {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content=format_error_response(
            code=f"HTTP_{exc.status_code}",
            message=exc.detail if isinstance(exc.detail, str) else "요청 처리 중 오류가 발생했습니다.",
            hint=request.url.path
        )
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logging.exception(f"[UnhandledException] {exc}")
    return JSONResponse(
        status_code=500,
        content=format_error_response("INTERNAL_SERVER_ERROR", "서버 내부 오류가 발생했습니다.", str(exc))
    )

# ✅ API 라우터 등록
app.include_router(solution_router, prefix="/api/ai/v1")
app.include_router(feedback_router, prefix="/api/ai/v2")
app.include_router(interview_router, prefix="/api/ai/v2")
app.include_router(summary_router, prefix="/api/ai/v2")

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)