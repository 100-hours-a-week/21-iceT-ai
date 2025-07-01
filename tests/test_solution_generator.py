# 테스트 코드
# 실행 방법 : python -m pytest -s tests/test_solution_generator.py

import pytest
from src.schemas.v1.solution_schema import SolutionRequest
from src.crawler.v1.solution_generater import generate_explanation
from src.crawler.v1.post_client import post_to_backend

@pytest.mark.asyncio
async def test_explain_solutions():
    # 처리할 문제들을 dict 형태로 리스트에 나열
    raw_problems = [
        {
            "problem_number": 1109,
            "title": "섬",
            "description": (
                "지도가 주어졌을 때, 섬의 높이를 계산하는 문제이다. "
                "섬은 'x'가 가로, 세로, 대각선으로 연결된 그룹으로 정의되며, "
                "섬 A가 다른 섬 B를 포함하면 B를 포함하는 A의 높이는 B의 높이 + 1이다. "
                "지도에서 각 높이에 해당하는 섬의 개수를 출력한다."
            ),
            "input": (
                "첫째 줄에 N과 M이 주어진다. "
                "둘째 줄부터 N개의 줄에 지도가 주어진다. "
                "지도는 'x' 또는 '.'으로 이루어져 있고, N과 M은 50 이하의 자연수이다."
            ),
            "output": (
                "높이가 0인 섬의 개수부터 최대 높이에 해당하는 섬의 개수까지 공백으로 구분하여 출력한다. "
                "섬이 하나도 없으면 -1을 출력한다."
            ),
            "input_example": (
                "5 5\n"
                "xxxxx\n"
                "x...x\n"
                "x.x.x\n"
                "x...x\n"
                "xxxxx\n"
            ),
            "output_example": (
                "1 1\n"
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