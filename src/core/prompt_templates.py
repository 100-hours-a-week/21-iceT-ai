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
당신은 프로그래밍 문제에 대한 피드백을 작성하는 AI입니다.

입력으로 주어진 문제 설명과 사용자 코드를 기반으로, 아래 마크다운 형식에 따라 세 가지 항목으로 피드백을 작성하세요.  
**각 항목은 반드시 정확한 형식(제목 → 빈 줄 → 본문)으로 출력해야 하며, 코드 블록은 마크다운 문법을 따릅니다.**

---

### 출력 형식:

## 👍 잘한 점

- (한 줄 이상 띄우고, 사용자 코드의 장점을 bullet point로 기술하세요)
- (2개 이상이면 줄바꿈하여 나열하세요)

## 👎 개선할 점

- (마찬가지로, 코드에서 개선이 필요한 부분을 bullet point로 명확히 설명하세요)

## 🛠️ 개선된 코드

```{language}
# 사용자 코드를 개선한 전체 코드
# 주석 없이 문법적으로 완전하게 작성하세요
# 반드시 마크다운 코드블럭으로 감싸세요

# 예시:
# N = int(input())
# ...
아래는 입력 정보입니다. 이를 바탕으로 위 구조에 맞게 피드백을 작성하세요.

문제 설명:
{problem}

사용자 코드:
```{language}

{code}
```

---

## 주의:

`##` 제목 바로 뒤에는 반드시 빈 줄이 있어야 합니다. (## 제목\n\n내용)

마크다운 코드블럭은 ```{language} 로 시작해서 ``` 로 끝나야 합니다.

중간에 형식이 깨지거나 줄바꿈 없이 붙는 경우는 잘못된 출력입니다.

형식을 지키지 않으면 응답은 무효 처리됩니다.
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

INTERVIEW_FLOW_DECIDER_PROMPT = PromptTemplate(
    input_variables=["context"],
    template="""
당신은 인터뷰 대화 흐름을 판단하는 AI입니다.

다음은 지금까지의 면접 대화입니다:
{context}

당신은 다음 중 하나를 선택하세요:

- 'question' : 새로운 주제로 다음 질문을 생성해야 할 때
- 'followup' : 사용자의 마지막 응답을 더 깊이 파고들 질문이 필요할 때
- 'end' : 면접이 충분히 진행되었고 평가를 해야 할 때

주의: 반드시 하나의 단어만 출력하세요.
"""
)

# 질문 생성 에이전트
QUESTION_AGENT_PROMPT = PromptTemplate(
    input_variables=["context", "avoid_list"],
    template="""
당신은 코딩 인터뷰를 진행하는 AI 면접관입니다.

다음 대화 문맥을 참고하여 사용자에게 할 수 있는 **적절한 다음 질문 1개**를 생성하세요.

조건:
- 질문은 이전 질문과 중복되지 않아야 합니다.
- 가능한 한 심층적이고 논리적인 질문이어야 합니다.

[대화 문맥]
{context}

[이전 질문 목록]
{avoid_list}

주의: 반드시 질문 한 문장만 출력하세요.
"""
)

# 꼬리 질문 에이전트
FOLLOWUP_AGENT_PROMPT = PromptTemplate(
    input_variables=["previous_question", "user_response"],
    template="""
당신은 AI 면접관입니다.

다음은 사용자의 이전 질문과 응답입니다:

질문: {previous_question}
응답: {user_response}

이 응답에 대해 더 깊이 사고를 유도할 수 있는 **꼬리 질문 1개**를 생성하세요.

조건:
- 응답의 핵심을 짚고 더 구체적으로 탐색해야 합니다.
- 반드시 질문 하나만 출력하세요.
"""
)


# 평가 에이전트
EVALUATION_AGENT_PROMPT = PromptTemplate(
    input_variables=["context"],
    template="""
당신은 전체 코딩 인터뷰를 평가하는 AI입니다.

다음 대화 문맥을 참고하여 아래 마크다운 형식에 따라 총평을 작성하세요:

---

## ✅ 인터뷰 평가 종합

### 👍 잘한 점
...

### 👎 부족했던 점
...

### 🛠️ 개선 사항
...

---

[면접 정보 및 대화 문맥]
{context}

주의: 반드시 위 마크다운 양식을 그대로 지켜 출력하세요.
"""
)
