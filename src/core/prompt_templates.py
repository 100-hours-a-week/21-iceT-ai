from langchain_core.prompts import PromptTemplate

# ✅ 해설 프롬프트 (LangChain용 structured output)
SOLUTION_PROMPT = PromptTemplate(
    template="""
다음 문제 정보를 바탕으로 문제 해설을 작성하세요.
응답은 반드시 아래 JSON 예시와 **정확히 같은 키 이름과 타입**을 따르세요.
내용은 한국어나 영어로 작성하고 절대 중국어를 포함하지 마세요.
마크다운이나 설명은 포함하지 마세요.

예시:
{
  "problemNumber": 1000,
  "problem_check": {
    "problem_description": "문제 개요를 여기에 작성",
    "algorithm": "사용된 알고리즘 또는 접근법"
  },
  "problem_solving": "문제 풀이 단계를 서술하는 문자열",
  "solution_code": {
    "python": "파이썬 코드 문자열",
    "cpp": "C++ 코드 문자열",
    "java": "Java 코드 문자열"
  }
}

문제 번호   : {problem_number}
제목       : {title}
설명       : {description}
입력       : {input}
출력       : {output}
입력 예시   : {input_example}
출력 예시   : {output_example}
""",
    input_variables=[
        "problem_number", "title", "description",
        "input", "output", "input_example", "output_example"
    ]
)

# ✅ 코드 피드백 프롬프트
FEEDBACK_PROMPT = PromptTemplate(
    template="""
당신은 코드 리뷰어입니다. 아래 문제 설명과 사용자 코드를 보고 다음 항목을 **반드시 JSON 형식으로만** 출력하세요:

1. 문제의 요지를 요약한 문장형 제목 (title)
2. 잘한 점 2가지 (good)
3. 개선할 점 2가지 (bad)
4. 개선된 코드 (improved_code)

출력 예시는 다음과 같아야 합니다:

{
  "title": "반복문에서 변수 재사용 오류",
  "good": ["코드 구조가 간결합니다.", "입력 처리를 적절히 했습니다."],
  "bad": ["정수 변환이 누락되었습니다.", "입력 검증이 없습니다."],
  "improved_code": "수정된 전체 코드 문자열"
}

응답은 반드시 한국어나 영어로 작성해야 하며, 절대 중국어를 포함하지 마세요.
추가 설명, 마크다운, 문장 등은 절대 포함하지 마세요. 정확한 JSON만 출력하세요.

문제 제목: {title}
문제 설명: {description}
입력 조건: {input_rule}
출력 조건: {output_rule}
입력 예시: {sample_input}
출력 예시: {sample_output}

사용자 코드 ({code_language}):
{code}
""",
    input_variables=[
        "title", "description", "input_rule", "output_rule",
        "sample_input", "sample_output", "code", "code_language"
    ]
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

질문은 반드시 하나만

질문의 초점은 문제 풀이 방식, 시간 복잡도, 예외 처리 등에 둬도 좋아

여는 말이나 맺는 말 없이, 문장 하나만 출력

질문은 반드시 한국어나 영어로 작성하고, 절대 중국어를 포함하지 마세요

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
너는 모의 기술 면접관이야. 아래는 지금까지의 면접 대화야.
가장 마지막 답변을 바탕으로, 다음 면접 질문을 하나만 작성해줘.

조건:

질문은 하나만

여는 말이나 맺는 말 없이, 문장 하나만 출력

질문은 반드시 한국어나 영어로 작성하고, 절대 중국어를 포함하지 마세요

면접 대화:
{history}
""".strip()

# ✅ 모의 면접 - 총평 프롬프트
INTERVIEW_REVIEW_PROMPT = """
다음은 면접관과 지원자의 대화입니다:

{history}

이 면접 내용을 평가해서 아래 JSON 형식에 맞춰 응답하세요.
정확한 JSON 구조를 따르고, 불필요한 문장이나 마크다운 없이 순수한 JSON만 출력하세요.
응답은 반드시 한국어나 영어로 작성되어야 하며, 절대 중국어를 포함하지 마세요.

{
    "good": ["지원자의 강점 1", "지원자의 강점 2"],
    "bad": ["지원자의 약점 1", "지원자의 약점 2"],
    "improvement": ["지원자가 개선해야 할 점 1", "개선해야 할 점 2"]
}
""".strip()
