# 테스트 코드
# 실행 방법 : python -m pytest -s tests/test_solution_generator.py

import pytest
from src.schemas.solution_schema import SolutionRequest
from src.crawler.solution_generater import generate_explanation

@pytest.mark.asyncio
async def test_explain_solution():
    # 테스트용 문제 정의
    test_problem = {
        "problem_number": 5430,
        "title": "AC",
        "description": (
            "AC는 정수 배열에 연산을 수행하기 위해 만들어진 언어입니다. "
            "이 언어에는 두 가지 함수 R(뒤집기)과 D(버리기)가 있습니다.\n\n"
            "함수 R은 배열에 있는 수의 순서를 뒤집는 함수이고, "
            "D는 배열의 첫 번째 수를 버리는 함수입니다. "
            "배열이 비어있는데 D를 사용하면 에러가 발생합니다.\n\n"
            "함수들은 조합해서 한 번에 연속 수행할 수 있습니다. "
            "예를 들어, “AB”는 A를 수행한 다음에 바로 이어서 B를 수행하는 함수입니다. "
            "“RDD”는 배열을 뒤집은 다음 처음 두 수를 버리는 연산을 의미합니다.\n\n"
            "배열의 초기값과 수행할 함수가 주어졌을 때, 최종 결과를 구하는 프로그램을 작성하세요."
        ),
        "input": (
            "첫째 줄에 테스트 케이스의 개수 T가 주어집니다. (T ≤ 100)\n"
            "각 테스트 케이스 첫째 줄에는 수행할 함수 p가 주어집니다. (1 ≤ |p| ≤ 100,000)\n"
            "다음 줄에는 배열에 들어있는 수의 개수 n이 주어집니다. (0 ≤ n ≤ 100,000)\n"
            "다음 줄에는 [x1,x2,…,xn] 형태로 배열에 들어 있는 정수가 주어집니다. (1 ≤ xi ≤ 100)\n"
            "전체 테스트 케이스에 걸쳐 p의 길이 합과 n의 합은 700,000을 넘지 않습니다."
        ),
        "output": (
            "각 테스트 케이스에 대해, 주어진 정수 배열에 함수를 모두 수행한 결과를 출력합니다. "
            "만약 중간에 D 연산을 수행할 때 배열이 비어 있으면 “error”를 출력하세요."
        ),
        "input_example": (
            "4\n"
            "RDD\n"
            "4\n"
            "[1,2,3,4]\n"
            "DD\n"
            "1\n"
            "[42]\n"
            "RRD\n"
            "6\n"
            "[1,1,2,3,5,8]\n"
            "D\n"
            "0\n"
            "[]"
        ),
        "output_example": (
            "[2,1]\n"
            "error\n"
            "[1,2,3,5,8]\n"
            "error"
        )
    }

    request = SolutionRequest(**test_problem)
    response = await generate_explanation(request)
    # response = await explain_solution(request)

    print("문제 개요:\n", response.problem_check.problem_description)
    print("사용 알고리즘:\n", response.problem_check.algorithm)
    print("풀이 단계:\n", response.problem_solving)
    print("정답 코드 (Python):\n", response.solution_code.python)