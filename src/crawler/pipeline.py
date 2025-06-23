from src.crawler.request_mapper import to_solution_request
from src.crawler.solution_generater import generate_explanation
from src.crawler.post_client import post_to_backend

# 크롤링 후 문제 데이터를 받아 해설을 생성하고 백엔드에 POST 요청을 보내는 파이프라인 함수
async def crawl_generate_post(problem_data: dict, language="python"):
    req = to_solution_request(problem_data, language)
    response = await generate_explanation(req)
    post_to_backend(problem_data["problem_number"], response)