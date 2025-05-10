from langchain_core.prompts import PromptTemplate

<<<<<<< HEAD
SOLUTION_PROMPT = """
너는 코드 문제를 해설해주는 AI야. 아래 정보를 바탕으로 다음 4가지 항목을 출력해줘.

1. 문제 확인 (문제에서 반드시 지켜야 하는 핵심 조건을 정리)
2. 문제 해결 (이 문제를 해결하기 위한 핵심 알고리즘 설명)
3. 코멘트 (현재 사용자의 코드가 문제를 해결하고 있는지에 대한 피드백)
4. 정답 코드 (선택한 언어 기준으로 정답이 되는 코드)

다음 형식에 맞춰 출력해줘:

문제 확인:
...

문제 해결:
...

코멘트:
...

정답 코드:
```
{code_language}
```{
...
문제 제목: {title}
문제 설명: {description}
입력 조건: {input_rule}
출력 조건: {output_rule}
입력 예시: {sample_input}
출력 예시: {sample_output}
사용자 코드:
{code}
"""

FEEDBACK_PROMPT = PromptTemplate(
    template="""
아래 문제 설명과 코드에 대해 피드백을 JSON 형식으로 작성하세요.

- 출력 형식은 반드시 다음과 같아야 합니다:
    ### 잘한점
    - 항목1
    - 항목2

    ### 개선해야 할 점
    - 항목1
    - 항목2
=======
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
>>>>>>> origin/dev

    ### 개선된 코드
    `코드블럭`

- 추가 설명은 절대 포함하지 마세요.

문제 제목: {title}
문제 번호: {number}
문제 설명: {description}
입력: {input_rule}
출력: {output_rule}
입력 예시: {sample_input}
출력 예시: {sample_output}

사용자 코드 ({code_language}):
{code}
""",
    input_variables=[
<<<<<<< HEAD
        "title", "number", "description",
        "input_rule", "output_rule",
        "sample_input", "sample_output",
        "code", "code_language"
=======
    "problem_number",
    "title",
    "description",
    "input",
    "output",
    "input_example",
    "output_example",
>>>>>>> origin/dev
    ],
)

FEEDBACK_CHAT_PROMPT = """
너는 사용자의 코드와 문제에 대해 피드백을 주고받는 친절한 챗봇이야.
지금까지의 대화를 참고해 적절하게 응답해줘.

{history}

사용자: {user_input}
AI:
""".strip()

INTERVIEW_START_PROMPT = PromptTemplate(
    template="""
너는 코딩 테스트를 기반으로 한 모의 면접관이야.
아래 문제 정보와 코드 내용을 바탕으로, 첫 면접 질문을 하나 작성해줘.

조건:
- 질문은 하나만 작성
- 질문의 초점은 문제 풀이 방식, 시간 복잡도, 예외 처리 등에 둬도 좋아
- 반드시 문장만 출력하고, 여는 말·맺는 말 없이 질문만 출력

문제 제목: {title}
문제 번호: {number}
문제 설명: {description}
입력 조건: {input_rule}
출력 조건: {output_rule}
입력 예시: {sample_input}
출력 예시: {sample_output}

사용자 코드 ({code_language}):
{code}
""",
    input_variables=[
        "title", "number", "description",
        "input_rule", "output_rule",
        "sample_input", "sample_output",
        "code", "code_language"
    ]
)

INTERVIEW_FOLLOWUP_PROMPT = """
너는 면접관이야. 아래는 지금까지의 면접 대화야.
가장 마지막 답변을 바탕으로, 다음 면접 질문을 하나만 작성해줘.

조건:
- 질문은 하나만
- 문장만 출력하고 여는 말·맺는 말 없이

면접 대화:
{history}
""".strip()

INTERVIEW_REVIEW_PROMPT = """
너는 면접관이야. 지금까지의 면접 대화를 읽고 총평을 작성해줘.

조건:
- 출력 형식은 반드시 다음과 같아야 해:

###잘한점-
- 항목1
- 항목2

###아쉬운 점-
- 항목1
- 항목2

###개선 방향성-
- 항목1
- 항목2

면접 대화:
{history}
""".strip()
