# 테스트 코드
# 실행 방법 : python -m pytest -s tests/test_solution_generator_v2.py

import pytest
from schemas.v2.solution_schema_v2 import SolutionRequest
from crawler.v2.solution_generater_v2 import generate_explanation
from crawler.v2.post_client_v2 import post_to_backend

@pytest.mark.asyncio
async def test_explain_solutions():
    # 처리할 문제들을 dict 형태로 리스트에 나열
    raw_problems = [
        {
            "problem_number": 1459,
            "title": "걷기",
            "description": (
                "세준이는 (0, 0)에서 출발하여 (X, Y)에 있는 집으로 가려고 한다. "
                "도시에는 모든 정수 x 좌표마다 세로 도로, 모든 정수 y 좌표마다 가로 도로가 있고, "
                "세준이는 한 블록을 가로・세로로 이동하는 데 W의 시간이 걸리며, "
                "한 블록을 대각선으로 가로지르는 데 S의 시간이 걸린다. "
                "집까지 가는 최소 시간을 구하라."
            ),
            "input": (
                "첫째 줄에 X Y W S가 주어진다. "
                "X와 Y는 음이 아닌 정수(≤1,000,000,000), W와 S는 자연수(≤10,000)이다."
            ),
            "output": (
                "첫째 줄에 집까지 가는 최소 시간을 출력한다."
            ),
            "input_example": (
                "4 2 3 10\n"
            ),
            "output_example": (
                "18\n"
            )
        },
    ]

    for prob in raw_problems:
        request = SolutionRequest(**prob)
        response = await generate_explanation(request)
        success = post_to_backend(request.problem_number, response)
        assert success, f"백엔드 전송에 실패했습니다: {request.problem_number}"

        print("문제 개요:\n", response.problem_check.problem_description)
        print("사용 알고리즘:\n", response.problem_check.algorithm)
        print("풀이 단계:\n", response.problem_solving)
        print("정답 코드 (Python):\n", response.solution_code.python)