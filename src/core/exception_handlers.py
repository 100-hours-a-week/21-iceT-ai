from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

logger = logging.getLogger(__name__)

def format_error_response(code: str, message: str, hint: str = ""):
    return {
        "error": {
            "code": code,
            "message": message,
            "hint": hint
        }
    }

async def validation_exception_handler(request: Request, exc: ValidationError):
    logger.warning(f"[ValidationError] {exc}")
    return JSONResponse(
        status_code=400,
        content=format_error_response(
            "INVALID_REQUEST",
            "입력 형식이 잘못되었습니다. problem_number는 필수입니다.",
            "필수 필드 누락 여부를 확인하세요."
        )
    )

async def value_error_handler(request: Request, exc: ValueError):
    logger.error(f"[ValueError] {exc}")
    return JSONResponse(
        status_code=422,
        content=format_error_response(
            "LLM_PARSE_FAILED",
            "모델의 응답을 처리하는 중 문제가 발생했습니다.",
            "출력 형식을 확인하거나 프롬프트를 점검하세요."
        )
    )

async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception(f"[UnhandledException] {exc}")
    return JSONResponse(
        status_code=500,
        content=format_error_response(
            "INTERNAL_SERVER_ERROR",
            "모델 추론 중 오류가 발생했습니다.",
            "서버 로그를 확인하거나 모델 상태를 점검하세요."
        )
    )

async def timeout_exception_handler(request: Request, exc: TimeoutError):
    logger.error(f"[TimeoutError] {exc}")
    return JSONResponse(
        status_code=504,
        content=format_error_response(
            "MODEL_TIMEOUT",
            "모델 응답이 제한 시간 내에 도착하지 않았습니다.",
            "서버 성능 또는 모델 상태를 확인하세요."
        )
    )

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.error(f"[HTTPException] {exc}")
    return JSONResponse(
        status_code=exc.status_code,
        content=format_error_response(
            code="HTTP_" + str(exc.status_code),
            message=exc.detail if isinstance(exc.detail, str) else "예기치 못한 오류입니다.",
            hint=request.url.path
        )
    )