from langchain_core.prompts import PromptTemplate

# 백준 문제 정보를 기반으로 해설을 생성하는 프롬프트 템플릿
SOLUTION_PROMPT = PromptTemplate(
    template="""
    아래 백준 문제 정보를 바탕으로, 출력 순서에 따라 **JSON 형식**으로만 해설을 작성하세요.

    출력 순서는 다음과 같습니다.
    1. problemNumber(문제 번호)
    2. problem_check(문제 개요 및 알고리즘 설명)
    3. problem_solving(단계별 구체적인 풀이 방법. 구체적일수록 좋음)
    4. solution_code(정답 코드를 python, c++, java로 각각 작성)

    문제 번호   : {problem_number}
    제목       : {title}
    설명       : {description}
    입력       : {input}
    출력       : {output}
    입력 예시   : {input_example}
    출력 예시   : {output_example}

    **주의**: 반드시 JSON 딕셔너리만 반환하고, 추가 설명·주석 금지
    """,
    input_variables=[
    "problem_number",
    "title",
    "description",
    "input",
    "output",
    "input_example",
    "output_example",
    ],
)