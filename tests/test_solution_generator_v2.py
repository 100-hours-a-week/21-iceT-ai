# 테스트 코드
# 실행 방법 : python -m pytest -s tests/test_solution_generator_v2.py

import pytest
from src.schemas.solution_schema import SolutionRequest
from src.crawler.solution_generater import generate_explanation
from src.crawler.post_client import post_to_backend

@pytest.mark.asyncio
async def test_explain_solutions():
    # 처리할 문제들을 dict 형태로 리스트에 나열
    raw_problems = [
        {
            "problem_number": 16173,
            "title": "점프왕 쩰리 (Small)",
            "description": (
                "‘쩰리’는 점프하는 것을 좋아하는 젤리다. 단순히 점프하는 것에 지루함을 느낀 ‘쩰리’는 새로운 점프 게임을 해보고 싶어 한다.\n\n"
                "게임 구역은 N×N 크기의 정사각형이며, 각 칸에는 이동 거리(0 이상 100 이하) 또는 목표 지점(-1)이 쓰여 있다.\n"
                "‘쩰리’는 맨 왼쪽 위 칸(1,1)에서 시작하며, 한 번에 이동할 수 있는 칸 수는 현재 칸에 쓰여 있는 숫자와 정확히 같다.\n"
                "이동 가능 방향은 오른쪽 또는 아래뿐이며, 구역을 벗어나면 즉시 패배한다.\n"
                "목표 지점 칸(-1)에 도달하면 게임에서 즉시 승리한다.\n\n"
                "주어진 맵에서 ‘쩰리’가 목표 지점에 도달할 수 있는지 판단하는 프로그램을 작성하시오."
            ),
            "input": (
                "첫째 줄에 게임 구역의 크기 N이 주어진다. (2 ≤ N ≤ 3)\n"
                "그 다음 N개의 줄에 게임판 정보가 주어진다.\n"
                "각 줄에는 N개의 정수가 주어지며, 마지막 칸(골인 지점)에는 -1이 쓰여 있고, 나머지는 0 이상 100 이하이다."
            ),
            "output": (
                "‘쩰리’가 목표 지점에 도달할 수 있으면 “HaruHaru”를, 도달할 수 없으면 “Hing”을 출력한다."
            ),
            "input_example": (
                "3\n"
                "1 1 10\n"
                "1 5 1\n"
                "2 2 -1\n"
            ),
            "output_example": (
                "HaruHaru\n"
            )
        },
        # 나중에 여기에 raw_problems.append(다른 문제 dict) 추가 가능
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