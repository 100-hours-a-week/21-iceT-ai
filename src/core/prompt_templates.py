from langchain_core.prompts import PromptTemplate

SOLUTION_PROMPT = PromptTemplate(
    template="""
    아래 백준 문제 정보를 바탕으로, **JSON 형식**으로만 해설을 작성하세요.

    출력 순서는 다음과 같습니다.
    1. language
    2. problem_description(문제 개요 요약해서 작성)
    3. algorithm(사용된 알고리즘 구체적으로)
    4. problem_solving(단계별 구체적인 풀이 방법. 구체적일수록 좋음)
    5. solution_code(정답 코드)

    문제 번호   : {problem_number}
    제목       : {title}
    설명       : {description}
    입력 예시   : {input_example}
    출력 예시   : {output_example}
    언어       : {language}

    **주의**: 반드시 JSON 딕셔너리만 반환하고, 추가 설명·주석 금지
    """,
    input_variables=[
    "problem_number",
    "title",
    "description",
    "input_example",
    "output_example",
    "language",
    ],
)