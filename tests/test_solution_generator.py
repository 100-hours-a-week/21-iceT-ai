import pytest
from src.schemas.solution_schema import SolutionRequest
from src.services.solution_service import explain_solution

@pytest.mark.asyncio
async def test_explain_solution():
    # 테스트용 문제 정의
    test_problem = {
        "problem_number": 1931,
        "title": "회의실 배정",
        "description": (
            "한 개의 회의실이 있다. 이를 사용하고자 하는 N개의 회의에 대해 회의실 사용표를 만들려고 한다. "
            "각 회의에는 시작 시간과 끝나는 시간이 있다. 각 회의가 겹치지 않게 하면서 회의실을 사용할 수 있는 "
            "최대 개수를 구하는 문제이다. 회의는 한번 시작하면 중간에 중단될 수 없고, 한 회의가 끝나는 것과 "
            "동시에 다음 회의가 시작될 수 있다."
        ),
        "input": (
            "첫째 줄에 회의의 수 N(1 ≤ N ≤ 100,000)이 주어진다.\n"
            "둘째 줄부터 N+1 줄까지 각 회의의 정보가 주어지는데, "
            "각 정보는 두 개의 정수 S와 T로 이루어져 있으며, "
            "회의의 시작 시간과 끝나는 시간이다. (0 ≤ S < T ≤ 10^9)"
        ),
        "output": "회의실을 사용할 수 있는 최대 회의 수를 출력한다.",
        "input_example": "11\n1 4\n3 5\n0 6\n5 7\n3 8\n5 9\n6 10\n8 11\n8 12\n2 13\n12 14",
        "output_example": "4",
    }

    request = SolutionRequest(**test_problem)
    response = await explain_solution(request)

    print("🧩 문제 개요:\n", response.problem_check.problem_description)
    print("🧠 사용 알고리즘:\n", response.problem_check.algorithm)
    print("🪜 풀이 단계:\n", response.problem_solving)
    print("💻 정답 코드 (Python):\n", response.solution_code.python)