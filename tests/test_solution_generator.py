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
        "problem_number": 1049,
        "title": "기타줄",
        "description": (
            "Day Of Mourning의 기타리스트 강토가 사용하는 기타에서 N개의 줄이 끊어졌다. "
            "따라서 새로운 줄을 사거나 교체해야 한다. 강토는 되도록이면 돈을 적게 쓰려고 한다. "
            "6줄 패키지를 살 수도 있고, 1개 또는 그 이상의 줄을 낱개로 살 수도 있다.\n\n"
            "끊어진 기타줄의 개수 N과 기타줄 브랜드 M개가 주어지고, 각각의 브랜드에서 파는 "
            "기타줄 6개가 들어있는 패키지의 가격, 낱개로 살 때의 가격이 주어질 때, "
            "적어도 N개를 사기 위해 필요한 돈의 수를 최소로 하는 프로그램을 작성하시오."
        ),
        "input": (
            "첫째 줄에 N과 M이 주어진다. N은 100보다 작거나 같은 자연수이고, "
            "M은 50보다 작거나 같은 자연수이다.\n"
            "둘째 줄부터 M개의 줄에는 각 브랜드의 패키지 가격과 낱개의 가격이 공백으로 구분되어 주어진다. "
            "가격은 0보다 크거나 같고, 1,000보다 작거나 같은 정수이다."
        ),
        "output": (
            "기타줄을 적어도 N개 사기 위해 필요한 돈의 최솟값을 출력한다."
        ),
        "input_example": (
            "4 2\n"
            "12 3\n"
            "15 4\n"
        ),
        "output_example": (
            "12\n"
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