# 백앤드 POST 요청 전송

import requests
from src.schemas.solution_schema import SolutionResponse

def post_to_backend(problem_id: int, response: SolutionResponse):
    url = "https://ktbkoco.com/api/backend/v1/solution"
    headers = {"Content-Type": "application/json"}

    res = requests.post(url, json=response.model_dump(), headers=headers)
    print(f"[{problem_id}] POST 응답: {res.status_code} - {res.text}")