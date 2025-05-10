from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
<<<<<<< HEAD
=======
from fastapi.exceptions import RequestValidationError
>>>>>>> origin/dev
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

<<<<<<< HEAD
=======

# 로그 출력 설정
>>>>>>> origin/dev
def format_error_response(code: str, message: str, hint: str = ""):
    return {
        "error": {
            "code": code,
            "message": message,
            "hint": hint
        }
    }

<<<<<<< HEAD
def add_exception_handlers(app: FastAPI):
=======
# FastAPI 앱에 공통 예외 핸들러 등록
def add_exception_handlers(app: FastAPI):

    # FastAPI 내부의 RequestBody/Query 등 검증 실패
    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
        logging.warning(f"[RequestValidationError] {exc}")
        return JSONResponse(
            status_code=422,
            content=format_error_response(
                "REQUEST_VALIDATION_FAILED",
                "요청 JSON 구조가 잘못되었습니다. 필수 항목 또는 타입을 확인하세요.",
                hint=str(exc)
            )
        )

    # Pydantic 모델에서 발생하는 유효성 검증 오류
>>>>>>> origin/dev
    @app.exception_handler(ValidationError)
    async def validation_exception_handler(request: Request, exc: ValidationError):
        logging.warning(f"[ValidationError] {exc}")
        return JSONResponse(
            status_code=400,
            content=format_error_response(
                "INVALID_REQUEST",
                "입력 형식이 잘못되었습니다. 필수 필드를 확인하세요.",
                hint=str(exc)
            )
        )

<<<<<<< HEAD
=======
    # LLM 응답 파싱 실패나 로직 내 값 오류 발생 시
>>>>>>> origin/dev
    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        logging.error(f"[ValueError] {exc}")
        return JSONResponse(
            status_code=422,
            content=format_error_response(
                "LLM_PARSE_FAILED",
                "모델의 응답을 처리하는 중 오류가 발생했습니다.",
                hint=str(exc)
            )
        )

<<<<<<< HEAD
=======
    # FastAPI 내부의 HTTPException 발생 시
>>>>>>> origin/dev
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

<<<<<<< HEAD
=======
    # 모델 응답 시간 초과 시
>>>>>>> origin/dev
    @app.exception_handler(TimeoutError)
    async def timeout_exception_handler(request: Request, exc: TimeoutError):
        logging.error(f"[TimeoutError] {exc}")
        return JSONResponse(
            status_code=504,
            content=format_error_response(
                "MODEL_TIMEOUT",
                "모델 응답 시간이 초과되었습니다.",
                hint=str(exc)
            )
        )
<<<<<<< HEAD

=======
      
    # 기타 모든 예외 처리
>>>>>>> origin/dev
    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        logging.exception(f"[UnhandledException] {exc}")
        return JSONResponse(
            status_code=500,
            content=format_error_response(
                "INTERNAL_SERVER_ERROR",
                "서버 내부 오류가 발생했습니다.",
                hint=str(exc)
            )
        )