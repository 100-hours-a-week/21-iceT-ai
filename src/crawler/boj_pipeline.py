# 전체 오케스트레이션 함수

from src.services.solution_service import explain_solution
from src.schemas.solution_schema import SolutionRequest, SolutionResponse
from src.config import BACKEND_URL, BACKEND_TIMEOUT  #, SERVICE_API_KEY
import requests
import logging

logger = logging.getLogger(__name__)


# 크롤링된 dict → SolutionRequest 변환
def to_solution_request(problem_data: dict, language="python") -> SolutionRequest:
    return SolutionRequest(
        problem_number=problem_data["problem_number"],
        title=problem_data["title"],
        description=problem_data["description"],
        input=problem_data["input"],
        output=problem_data["output"],
        input_example=problem_data["input_example"][0],
        output_example=problem_data["output_example"][0],
    )


# GPT 해설 생성
async def generate_explanation(request: SolutionRequest) -> SolutionResponse:
    return await explain_solution(request)


# 백엔드 POST 요청 전송
def post_to_backend(problem_id: int, response: SolutionResponse):
    try:
        res = requests.post(
            BACKEND_URL,
            json=response.model_dump(),
            headers={
                "Content-Type": "application/json"
                # "X-API-KEY": SERVICE_API_KEY
            },
            timeout=BACKEND_TIMEOUT,
        )
        res.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"[{problem_id}] POST 요청 실패: {e}")
        return False

    logger.info(f"[{problem_id}] POST 성공: {res.status_code}")
    return True


# 전체 파이프라인 실행
async def crawl_generate_post(problem_data: dict, language="python"):
    req = to_solution_request(problem_data, language)
    response = await generate_explanation(req)
    post_to_backend(problem_data["problem_number"], response)
