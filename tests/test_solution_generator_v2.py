# 테스트 코드
# 실행 방법 : python -m pytest -s tests/test_solution_generator_v2.py

import pytest
from src.schemas.v2.solution_schema_v2 import SolutionRequest
from src.crawler.v2.solution_generater_v2 import generate_explanation
from src.crawler.v2.post_client_v2 import post_to_backend

@pytest.mark.asyncio
async def test_explain_solutions():
    # 처리할 문제들을 dict 형태로 리스트에 나열
    raw_problems = [
        {
            "problem_number": 14502,
            "title": "연구소",
            "description": (
                "인체에 치명적인 바이러스를 연구하던 연구소에서 바이러스가 유출되었다. "
                "바이러스는 상하좌우 인접한 칸으로 퍼져나간다. 일부 칸에는 벽을 세울 수 있다.\n\n"
                "연구소는 N×M 크기의 직사각형으로 나타낼 수 있으며, 각 칸은 빈 칸(0), 벽(1), 바이러스(2)로 이루어져 있다. "
                "연구소의 지도가 주어졌을 때, 벽을 3개 세워서 바이러스의 확산을 막을 수 있는 **안전 영역의 최대 크기**를 구하는 프로그램을 작성하시오."
            ),
            "input": (
                "첫째 줄에 지도의 세로 크기 N과 가로 크기 M이 주어진다. (3 ≤ N, M ≤ 8)\n"
                "둘째 줄부터 N개의 줄에 지도의 정보가 주어진다. "
                "0은 빈 칸, 1은 벽, 2는 바이러스를 의미한다."
            ),
            "output": (
                "벽을 3개 세운 뒤, 바이러스가 퍼질 수 없는 안전 영역의 최대 크기를 출력한다."
            ),
            "input_example": (
                "7 7\n"
                "2 0 0 0 1 1 0\n"
                "0 0 1 0 1 2 0\n"
                "0 1 1 0 1 0 0\n"
                "0 1 0 0 0 0 0\n"
                "0 0 0 0 0 1 1\n"
                "0 1 0 0 0 0 0\n"
                "0 1 0 0 0 0 0\n"
            ),
            "output_example": (
                "27\n"
            ),
            "algorithm": [
                "구현",
                "그래프 이론",
                "브루트포스 알고리즘",
                "그래프 탐색",
                "너비 우선 탐색",
                "격자 그래프"
            ]
        },
    ]

    for prob in raw_problems:
        request = SolutionRequest(**prob)
        response = await generate_explanation(request)
        if response is None:
            print("test - LLM 응답 없음")
            return None
        if not hasattr(response, "model_dump"):
            print("test - Pydantic 응답 아님:", type(response))
            return None
        # success = post_to_backend(request.problem_number, response)
        # assert success, f"백엔드 전송에 실패했습니다: {request.problem_number}"

        print("문제 개요:\n", response.problem_check.problem_description)
        print("사용 알고리즘:\n", response.problem_check.algorithm)
        print("풀이 단계:\n", response.problem_solving)
        print("정답 코드 (Python):\n", response.solution_code.python)