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

FEEDBACK_START_PROMPT = PromptTemplate(
    input_variables=["problem", "code", "language"],
    template="""
당신은 프로그래밍 문제에 대한 마크다운 피드백을 생성하는 AI입니다.

아래 문제 설명과 코드({language})를 분석하여 다음과 같은 마크다운 양식에 따라 응답하세요:

---

### 문제 요약
- 문제 제목 및 핵심 조건 요약

### 코드 분석
- 주요 로직 설명
- 시간/공간 복잡도 추정

### 개선 사항
- 코드 스타일/효율성/가독성 관점에서 개선점 제시

### 총평
- 전체적인 평가 멘트

---

문제:
{problem}

사용자 코드:
{code}

위 마크다운 양식을 반드시 그대로 따르고, 항목 제목은 그대로 출력하세요.
"""
)

FEEDBACK_ANSWER_PROMPT = PromptTemplate(
    input_variables=["context", "user_input"],
    template="""
다음은 이전 대화 내용입니다:
{context}

사용자가 이어서 질문했습니다:
"{user_input}"

기존 대화 흐름을 고려해 자연스럽고 논리적인 후속 응답을 제공하세요.
"""
)

INTERVIEW_START_PROMPT = PromptTemplate(
    input_variables=["problem", "language"],
    template="""
당신은 코딩 인터뷰를 진행하는 시뮬레이터입니다.

다음 문제에 대해 {language} 언어 기준으로 적절한 인터뷰 질문 한 가지를 생성하세요.
실제 면접에서 물어볼 수 있는 수준으로 문제의 핵심 개념을 짚는 질문을 하세요.

문제:
{problem}
"""
)

INTERVIEW_AGENT_PROMPT = PromptTemplate(
    input_variables=["agent_role", "context"],
    template="""
당신은 인터뷰 평가 역할 중 하나인 "{agent_role}" 역할을 맡고 있습니다.

다음은 인터뷰 중 사용자와 주고받은 대화 내용입니다:
{context}

이 역할에 따라 평가하거나 피드백을 작성하세요.
"""
)

INTERVIEW_END_PROMPT = PromptTemplate(
    input_variables=["context"],
    template="""
당신은 코딩 인터뷰의 전체 대화를 평가하는 AI입니다.

다음 대화 내용을 바탕으로 인터뷰에 대한 평가 리포트를 **마크다운 형식**으로 작성하세요.

---

## ✅ 인터뷰 평가 총평

### 👍 잘한 점
- 사용자가 잘한 점들을 간결하게 나열하세요 (2~4개)

### 👎 부족했던 점
- 부족했던 점이나 아쉬운 점을 나열하세요 (2~4개)

### 🛠️ 개선 사항
- 개선을 위한 조언 또는 다음 목표를 제시하세요 (2~4개)

---

전체 대화 내용:
{context}

주의: 위 마크다운 양식 그대로 출력하고, 텍스트 외 구조화 응답(JSON)은 하지 마세요.
"""
)

