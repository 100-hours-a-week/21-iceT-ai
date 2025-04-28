def get_solution_prompt(
    problem_number: int,
    title: str,
    description: str,
    input_example: str,
    output_example: str,
    language: str,
) -> str:
    """
    백준 문제 정보를 기반으로 JSON 포맷에 맞춰 해설을 생성하도록 하는 프롬프트
    """
    return f"""
아래 백준 문제 정보를 바탕으로, 다음 JSON 형식을 지켜서 해설을 생성해 주세요.

문제 번호: {problem_number}
제목: {title}
문제 설명: {description}
입력 예시: {input_example}
출력 예시: {output_example}
언어: {language}

출력 JSON 형식:
{{
  "language": "{language}",
  "problem_check": {{
    "problem_description": "문제 개요를 여기에 작성하세요.",
    "algorithm": "사용된 알고리즘을 여기에 작성하세요."
  }},
  "problem_solving": "단계별 풀이 방법을 여기에 작성하세요.",
  "solution_code": "정답 코드를 여기에 작성하세요."
}}
"""