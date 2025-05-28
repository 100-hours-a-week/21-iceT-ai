from langchain_core.prompts import PromptTemplate

# 백준 문제 정보를 기반으로 해설을 생성하는 프롬프트 템플릿
SOLUTION_PROMPT = PromptTemplate(
    template="""
    당신은 백준 문제에 대한 해설을 구조화된 형식으로 생성하는 AI입니다.
    아래 '백준 문제 정보'와 '참고 문서'를 바탕으로, 출력 순서에 따라 **JSON 형식**으로만 해설을 작성하세요.
    특히 알고리즘 설명 부분은 **반드시** '참고 문서' 내용을 직접 참조하여 정의, 작동 방법, 시간복잡도 등을 상세하게 설명해야 합니다.
    먄약 '참고 문서' 에 해당 알고리즘이 없다면, 해당 알고리즘을 직접 설명하세요.

    ---
    
    해설 출력 순서는 다음과 같습니다.
    {{
        "problemNumber": int,
        "problem_check": {{
            "problem_description": str,  // 문제 개요, 즉 문제 목표와 조건을 요약
            "algorithm": str             // 알고리즘 이름 + 정의 + 작동 방식 + 시간복잡도 (참고 문서에 해당 알고리즘이 존재하는 경우 반드시 참고 문서에 기반하여 기술)
        }},
        "problem_solving": str,        // 단계별 구체적인 풀이 전략 설명
        "solution_code": {{
            "python": str,               // 파이썬 정답 코드
            "cpp": str,                  // C++ 정답 코드
            "java": str                  // 자바 정답 코드
        }}
    }}

    ---
    
    각 필드 작성 규칙:

    - 'problem_description': 문제 목표와 조건을 요약
    - 'algorithm': 알고리즘 이름 + 정의 + 작동 방식 + 시간복잡도 (참고 문서에 없는 경우는 직접 설명)
    - 'problem_solving': 문제 풀이 방법을 단계별로 절차 설명 (구체적으로)
    - 'solution_code': 주석 없이 동작하는 완전한 정답 코드만 반환

    ---

    백준 문제 정보 : 
    문제 번호   : {problem_number}
    제목       : {title}
    설명       : {description}
    입력       : {input}
    출력       : {output}
    입력 예시   : {input_example}
    출력 예시   : {output_example}

    참고 문서 : 
    {context}

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
            "context",
    ],
)