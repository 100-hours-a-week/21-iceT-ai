# 백앤드 POST 요청 전송

import requests
from src.schemas.solution_schema import SolutionResponse

# TODO: URL 백앤드로 변경
def post_to_backend(problem_id: int, response: SolutionResponse):
    url = "http://localhost:8080/api/solution/save"
    headers = {"Content-Type": "application/json"}

    res = requests.post(url, json=response.model_dump(), headers=headers)
    print(f"[{problem_id}] POST 응답: {res.status_code} - {res.text}")