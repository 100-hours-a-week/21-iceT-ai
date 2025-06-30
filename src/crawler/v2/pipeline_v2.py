# 전체 오케스트레이션 함수

from src.crawler.v2.request_mapper_v2 import to_solution_request
from src.crawler.v2.solution_generater_v2 import generate_explanation
from src.crawler.v2.post_client_v2 import post_to_backend
import logging

logger = logging.getLogger(__name__)

# pydantic으로 변환 -> 해설 생성 -> 백엔드에 포스팅
async def crawl_generate_post(problem_data: dict, language="python"):
    req = to_solution_request(problem_data, language)
    response = await generate_explanation(req)
    if response is None:
        logger.error("pipeline - LLM 응답 없음")
        return None
    if not hasattr(response, "model_dump"):
        logger.error("pipeline - Pydantic 응답 아님:", type(response))
        return None
    post_to_backend(problem_data["problem_number"], response)