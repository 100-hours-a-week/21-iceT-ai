from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from models.solution_schema import SolutionRequest, SolutionResponse
from services.solution_service import explain_solution

router = APIRouter()

# POST /api/v1/solution
@router.post("/solution", response_model=SolutionResponse)
async def solution_endpoint(body: SolutionRequest):
    try:
        return await explain_solution(body)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#############################################
# TODO : 미완성
#############################################
async def solution_endpoint(body: SolutionRequest):
    try:
        return await explain_solution(body)
    except ValidationError as e:
        # Pydantic validation 실패 (입력 오류) → 400 에러
        raise HTTPException(
            status_code=400,
            detail={
                "error": {
                    "code": "INVALID_REQUEST",
                    "message": "입력 형식이 잘못되었습니다. 필수 필드를 확인하세요.",
                    "hint": str(e)
                }
            }
        )
    except Exception as e:
        # 서버 내부 오류 → 500 에러
        raise HTTPException(
            status_code=500,
            detail={
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "모델 추론 중 오류가 발생했습니다.",
                    "hint": str(e)
                }
            }
        )
