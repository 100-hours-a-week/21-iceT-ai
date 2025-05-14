# 백앤드 POST 요청 전송

import requests
from src.schemas.solution_schema import SolutionResponse
from src.config import BACKEND_URL, BACKEND_TIMEOUT, SERVICE_API_KEY
import logging

logger = logging.getLogger(__name__)

# 백엔드에 해설 데이터 전송
# - 요청 URL: BACKEND_URL
# - 요청 헤더: Content-Type: application/json
# - 요청 바디: SolutionResponse 스키마
# - 로깅: 성공 시 성공 메시지, 실패 시 실패 메시지
def post_to_backend(problem_id: int, response: SolutionResponse):
    try:
        res = requests.post(
            BACKEND_URL,
            json=response.model_dump(),
            headers={
                "Content-Type": "application/json" # ,
                # TODO: 백엔드한테 API 키 전달해야 함
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

