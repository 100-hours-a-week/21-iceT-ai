from langchain_core.prompts import PromptTemplate

# 백준 문제 정보를 기반으로 해설을 생성하는 프롬프트 템플릿
SOLUTION_PROMPT = PromptTemplate(
    template="""
    당신은 백준 문제에 대한 해설을 생성하는 AI입니다.
    아래 '백준 문제 정보'와 '참고 문서'를 바탕으로

    1) 문제 개요와 알고리즘 설명,
    2) 단계별 풀이 전략,
    3) Python, C++, Java 코드 예시
    
    를 마크다운 문법 없이 상세하게 작성해주세요. 

    특히 알고리즘 설명 부분은 '참고 문서' 내용을 바탕으로 작성하세요.

    --- 문제 정보 ---
    문제 번호    : {problem_number}
    제목        : {title}
    설명        : {description}
    입력 형식   : {input}
    출력 형식   : {output}
    입력 예시   : {input_example}
    출력 예시   : {output_example}

    --- 참고 문서 ---
    {context}
    """,

        input_variables=[
            "problem_number",
            "title",
            "description",
            "input",
            "output",
            "input_example",
            "output_example",
            "context",
    ],
)