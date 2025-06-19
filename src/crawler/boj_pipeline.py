# 전체 오케스트레이션 함수
import traceback
import json
import requests
from requests.exceptions import HTTPError, Timeout, ConnectionError, RequestException
from src.services.solution_service import explain_solution
from src.schemas.solution_schema import SolutionRequest, SolutionResponse
from src.config import settings
import requests
import logging

logger = logging.getLogger(__name__)


# 크롤링된 dict → SolutionRequest 변환
def to_solution_request(problem_data: dict, language="python") -> SolutionRequest:
    return SolutionRequest(
        problemNumber=problem_data["problem_number"],
        title=problem_data["title"],
        description=problem_data["description"],
        input=problem_data["input"],
        output=problem_data["output"],
        inputExample=problem_data["input_example"][0],
        outputExample=problem_data["output_example"][0],
    )


# GPT 해설 생성
async def generate_explanation(request: SolutionRequest) -> SolutionResponse:
    return await explain_solution(request)

def post_to_backend(problem_id: int, response: SolutionResponse):
    print(f"📤 문제 {problem_id} 해설 백엔드로 전송: {settings.backend_url}")
    try:
        res = requests.post(
            settings.backend_url,
            json=response.model_dump(by_alias=True),
            headers={
                "Content-Type": "application/json",
                "X-API-KEY": settings.service_api_key
            },
            timeout=60,
        )
        res.raise_for_status()

    except HTTPError as e:
        print(f"❌ [{problem_id}] HTTPError: {e}")
        print(f"↪ 응답 코드: {e.response.status_code}")
        print(f"↪ 응답 본문: {e.response.text}")
        return False
    except Timeout:
        print(f"❌ [{problem_id}] 요청 시간 초과 (Timeout)")
        return False
    except ConnectionError:
        print(f"❌ [{problem_id}] 연결 실패 (ConnectionError)")
        return False
    except RequestException as e:
        print(f"❌ [{problem_id}] 기타 요청 예외: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False
    else:
        print(f"✅ [{problem_id}] POST 성공: {res.status_code}")
        return True

# 전체 파이프라인 실행
async def crawl_generate_post(problem_data: dict, language="python"):
    req = to_solution_request(problem_data, language)
    response = await generate_explanation(req)
    post_to_backend(problem_data["problem_number"], response)
