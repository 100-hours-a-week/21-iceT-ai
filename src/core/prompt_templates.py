from langchain_core.prompts import PromptTemplate

# ✅ 해설 프롬프트 (LangChain용 structured output)
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

# ✅ 코드 피드백 프롬프트
FEEDBACK_PROMPT = PromptTemplate(
    template="""
당신은 코드 리뷰어입니다. 아래 문제 설명과 사용자 코드를 보고 다음 항목을 **반드시 JSON 형식으로만** 출력하세요:

1. 잘한 점 2가지 (good)
2. 개선할 점 2가지 (bad)
3. 개선된 코드 (improved_code)

형식 예시는 다음과 같습니다:

{
  "title": "문제 제목",
  "good": ["잘한 점 1", "잘한 점 2"],
  "bad": ["개선할 점 1", "개선할 점 2"],
  "improved_code": "여기에 전체 수정된 코드 문자열"
}

추가 설명, 마크다운, 문장 등은 절대 포함하지 마세요. 정확한 JSON만 출력하세요.

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
        "title",
        "number",
        "description",
        "input_rule",
        "output_rule",
        "sample_input",
        "sample_output",
        "code",
        "code_language",
    ],
)

# ✅ 자유 피드백 대화 프롬프트
FEEDBACK_CHAT_PROMPT = """
너는 사용자의 코드와 문제에 대해 피드백을 주고받는 친절한 챗봇이야.
지금까지의 대화를 참고해 적절하게 응답해줘.

{history}

사용자: {user_input}
AI:
""".strip()

# ✅ 모의 면접 - 첫 질문 프롬프트
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
        "title",
        "number",
        "description",
        "input_rule",
        "output_rule",
        "sample_input",
        "sample_output",
        "code",
        "code_language"
    ]
)

# ✅ 모의 면접 - 꼬리 질문 프롬프트
INTERVIEW_FOLLOWUP_PROMPT = """
너는 면접관이야. 아래는 지금까지의 면접 대화야.
가장 마지막 답변을 바탕으로, 다음 면접 질문을 하나만 작성해줘.

조건:
- 질문은 하나만
- 문장만 출력하고 여는 말·맺는 말 없이

면접 대화:
{history}
""".strip()

# ✅ 모의 면접 - 총평 프롬프트
INTERVIEW_REVIEW_PROMPT = """
다음은 면접관과 지원자의 대화입니다:

{history}

이 면접 내용을 평가해서 아래 JSON 형식에 맞춰 응답하세요.
정확한 JSON 구조를 따르고, 불필요한 문장이나 마크다운 없이 순수한 JSON만 출력하세요.

{
"good": ["지원자의 강점 1", "지원자의 강점 2"],
"bad": ["지원자의 약점 1", "지원자의 약점 2"],
"improvement": ["지원자가 개선해야 할 점 1", "개선해야 할 점 2"]
}
""".strip()
