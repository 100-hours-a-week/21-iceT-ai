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
        "problem_number": 7120,
        "title": "String 다국어",
        "description": (
            "컴퓨터 키보드 버튼이 걸려 동일 문자가 반복될 때, 예를 들어 “piano”가 “ppppppiaanooooo”로 바뀔 수 있습니다. "
            "주어진 문자열에서 연속된 동일 문자는 한 개만 남기고 나머지를 제거하여 원래 의도된 문자열을 복원하세요."
        ),
        "input": (
            "첫째 줄에 영문 소문자로만 이루어진 문자열이 주어집니다. "
            "문자열의 길이는 최대 250입니다."
        ),
        "output": (
            "중복이 제거된 수정된 문자열을 출력하세요."
        ),
        "input_example": "ppppppiaanooooo",
        "output_example": "piano"
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