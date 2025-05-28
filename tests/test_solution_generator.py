# 테스트 코드
# 실행 방법 : python -m pytest -s tests/test_solution_generator.py

import pytest
from src.schemas.solution_schema import SolutionRequest
from src.services.solution_service import explain_solution

@pytest.mark.asyncio
async def test_explain_solution():
    # 테스트용 문제 정의
    test_problem = {
        "problem_number": 14502,
        "title": "연구소",
        "description": (
            "인체에 치명적인 바이러스를 연구하던 연구소에서 바이러스가 유출되었다. 다행히 바이러스는 아직 퍼지지 않았고, "
            "바이러스의 확산을 막기 위해서 연구소에 벽을 세우려고 한다.\n\n"
            "연구소는 크기가 N×M인 직사각형이며, 각 칸은 빈 칸(0), 벽(1), 바이러스(2) 중 하나로 이루어져 있다. "
            "바이러스는 상하좌우로 인접한 빈 칸으로 퍼져나갈 수 있으며, 새로 세울 수 있는 벽의 개수는 정확히 3개이다.\n\n"
            "세 개의 벽을 적절히 세워 바이러스가 퍼질 수 없는 안전 영역(빈 칸)의 크기를 최대화하라.\n\n"
            "입력으로 지도의 정보가 주어질 때, 벽을 세운 뒤 바이러스가 퍼진 후 남게 되는 안전 영역의 최대 크기를 출력하는 프로그램을 작성하시오."
        ),
        "input": (
            "첫째 줄에 지도의 세로 크기 N과 가로 크기 M이 주어진다. (3 ≤ N, M ≤ 8)\n"
            "둘째 줄부터 N개의 줄에 지도의 정보가 주어진다. 각 줄은 M개의 정수로 구성되며, 0은 빈 칸, 1은 벽, 2는 바이러스를 의미한다.\n"
            "2의 개수는 2 이상 10 이하이며, 빈 칸의 개수는 최소 3개 이상이다."
        ),
        "output": (
            "바이러스가 퍼지지 않도록 벽을 세운 뒤, 안전 영역의 최대 크기를 출력한다."
        ),
        "input_example": "7 7\n2 0 0 0 1 1 0\n0 0 1 0 1 2 0\n0 1 1 0 1 0 0\n0 1 0 0 0 0 0\n0 0 0 0 0 1 1\n0 1 0 0 0 0 0\n0 1 0 0 0 0 0",
        "output_example": "27"
    }

    request = SolutionRequest(**test_problem)
    response = await explain_solution(request)

    print("문제 개요:\n", response.problem_check.problem_description)
    print("사용 알고리즘:\n", response.problem_check.algorithm)
    print("풀이 단계:\n", response.problem_solving)
    print("정답 코드 (Python):\n", response.solution_code.python)