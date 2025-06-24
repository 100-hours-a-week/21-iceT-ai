# 테스트 코드
# 실행 방법 : python -m pytest -s tests/test_solution_generator.py

import pytest
from src.schemas.solution_schema import SolutionRequest
from src.crawler.solution_generater import generate_explanation
from src.crawler.post_client import post_to_backend


@pytest.mark.asyncio
async def test_explain_solution():
    # 테스트용 문제 정의
    test_problem = {
        "problem_number": 1384,
        "title": "메시지",
        "description": (
            "Misfits 아카데미에서는 문제아 아이들이 서로에게 예의를 갖추도록 돕는 활동을 진행합니다. "
            "아이들은 원형으로 앉아 자신의 이름이 적힌 종이를 왼편으로 돌리며 서로에 대한 좋은 메시지를 남깁니다. "
            "하지만 일부 아이들은 규칙을 어기고 상대에게 불쾌한 메시지를 남기기도 합니다. "
            "각 아이가 받은 종이에는 그 아이의 이름과 함께, 위에서부터 순서대로 남겨진 P(좋은 메시지) 또는 N(나쁜 메시지)의 기록이 있습니다. "
            "누가 누구에게 나쁜 메시지를 남겼는지 추적하세요."
        ),
        "input": (
            "입력은 여러 개의 그룹으로 이루어져 있습니다. 각 그룹은 첫 줄에 아이의 수 n (5 ≤ n ≤ 20)이 주어지고, "
            "이후 n줄에 걸쳐 각 아이가 받은 종이의 정보가 순서대로 주어집니다. 각 줄은 이름과 메시지 n-1개(P 또는 N)로 구성됩니다. "
            "마지막 줄에 0이 입력되며, 이는 종료를 의미하고 처리하지 않습니다."
        ),
        "output": (
            "각 그룹에 대해 'Group x'를 먼저 출력합니다 (x는 그룹 번호). "
            "그 후 누가(A) 누구(B)에게 나쁜 메시지를 남겼는지 'A was nasty about B' 형식으로 출력합니다. "
            "나쁜 메시지가 없다면 'Nobody was nasty'를 출력합니다. "
            "각 그룹 출력 사이에는 빈 줄을 하나 둡니다."
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
    success = post_to_backend(test_problem["problem_number"], response)
    assert success, "백엔드 전송에 실패했습니다"
    # response = await explain_solution(request)

    print("문제 개요:\n", response.problem_check.problem_description)
    print("사용 알고리즘:\n", response.problem_check.algorithm)
    print("풀이 단계:\n", response.problem_solving)
    print("정답 코드 (Python):\n", response.solution_code.python)