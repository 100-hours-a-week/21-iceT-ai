# 테스트 코드
# 실행 방법 : python -m pytest -s tests/test_solution_generator.py

import pytest
from src.schemas.solution_schema import SolutionRequest
from src.crawler.solution_generater import generate_explanation

@pytest.mark.asyncio
async def test_explain_solution():
    # 테스트용 문제 정의
    test_problem = {
    "problem_number": 9999,
    "title": "메시지 다국어",
    "description": (
        "아이들이 원형으로 앉아 서로 종이를 넘기며 메시지를 작성합니다. "
        "좋은 메시지는 'P', 나쁜 메시지는 'N'으로 표기되고, 누가 누구에게 나쁜 말을 했는지 찾아야 합니다."
    ),
    "input": (
        "여러 그룹의 입력이 주어지며, 각 그룹은 첫 줄에 n (5 ≤ n ≤ 20), 다음 n줄은 n장의 종이 내용을 나타냅니다.\n"
        "각 줄은 이름과 함께 'P' 또는 'N'이 n-1개 주어지며, 마지막에 '0'이 입력되면 종료됩니다."
    ),
    "output": (
        "각 그룹마다 나쁜 말을 한 사람과 당한 사람을 출력합니다.\n"
        "형식은 'A was nasty about B'이며, 아무도 나쁜 말을 하지 않으면 'Nobody was nasty'를 출력합니다.\n"
        "각 그룹은 빈 줄로 구분됩니다."
    ),
    "input_example": (
        "5\n"
        "Ann P N P P\n"
        "Bob P P P P\n"
        "Clive P P P P\n"
        "Debby P N P P\n"
        "Eunice P P P P\n"
        "6\n"
        "Zheng P P P P P\n"
        "Yeng P P P P P\n"
        "Xiao P P P P P\n"
        "Will P P P P P\n"
        "Veronica P P P P P\n"
        "Utah P P P P P\n"
        "0"
    ),
    "output_example": (
        "Group 1\n"
        "Debby was nasty about Ann\n"
        "Bob was nasty about Debby\n"
        "\n"
        "Group 2\n"
        "Nobody was nasty"
    )
}


    request = SolutionRequest(**test_problem)
    response = await generate_explanation(request)
    # response = await explain_solution(request)

    print("문제 개요:\n", response.problemCheck.problem_description)
    print("사용 알고리즘:\n", response.problemCheck.algorithm)
    print("풀이 단계:\n", response.problemSolving)
    print("정답 코드 (Python):\n", response.solutionCode.python)
