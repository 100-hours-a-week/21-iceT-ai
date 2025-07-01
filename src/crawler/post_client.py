import requests
from src.schemas.v1.solution_schema import SolutionResponse
from src.config import BACKEND_SOLUTION_URL, BACKEND_TIMEOUT
import logging

logger = logging.getLogger(__name__)

# 백엔드에 POST 요청을 보내는 함수
def post_to_backend(problem_id: int, response: SolutionResponse):
    try:
        res = requests.post(
            BACKEND_SOLUTION_URL,
            json=response.model_dump(),
            headers={
                "Content-Type": "application/json"
            },
            timeout=BACKEND_TIMEOUT,
        )
        res.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"[{problem_id}] POST 요청 실패: {e}")
        return False
    
    logger.info(f"[{problem_id}] POST 성공: {res.status_code}")
    return True

