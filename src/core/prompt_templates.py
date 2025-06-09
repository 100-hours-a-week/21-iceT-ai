# src/core/prompt_templates.py
from langchain_core.prompts import PromptTemplate

# ✅ 문제 해설 프롬프트
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
        "problemCheck": {{
            "problemDescription": str,  // 문제 개요, 즉 문제 목표와 조건을 요약
            "algorithm": str             // 알고리즘 이름 + 정의 + 작동 방식 + 시간복잡도 (참고 문서에 해당 알고리즘이 존재하는 경우 반드시 참고 문서에 기반하여 기술)
        }},
        "problemSolving": str,        // 단계별 구체적인 풀이 전략 설명
        "solutionCode": {{
            "python": str,               // 파이썬 정답 코드
            "cpp": str,                  // C++ 정답 코드
            "java": str                  // 자바 정답 코드
        }}
    }}

    ---
    
    각 필드 작성 규칙:

    - 'problemDescription': 문제 목표와 조건을 요약
    - 'algorithm': 알고리즘 이름 + 정의 + 작동 방식 + 시간복잡도 (참고 문서에 없는 경우는 직접 설명)
    - 'problemSolving': 문제 풀이 방법을 단계별로 절차 설명 (구체적으로)
    - 'solutionCode': 주석 없이 동작하는 완전한 정답 코드만 반환

    ---

    백준 문제 정보 : 
    문제 번호   : {problemNumber}
    제목       : {title}
    설명       : {description}
    입력       : {input}
    출력       : {output}
    입력 예시   : {inputExample}
    출력 예시   : {outputExample}

    참고 문서 : 
    {context}

    **주의**: 반드시 JSON 딕셔너리만 반환하고, 추가 설명·주석 금지
    """,
        input_variables=[
            "problemNumber",
            "title",
            "description",
            "input",
            "output",
            "inputExample",
            "outputExample",
            "context",
    ],
)

# ✅ 코드 피드백 프롬프트
FEEDBACK_PROMPT = """
당신은 코드 리뷰어입니다. 아래 문제 설명과 사용자 코드를 보고 다음 항목을 **반드시 JSON 형식으로만** 출력하세요:

1. 문제의 요지를 요약한 문장형 제목 (title)
2. 잘한 점 2가지 (good)
3. 개선할 점 2가지 (bad)
4. 개선된 코드 (improved_code)

출력 예시는 다음과 같아야 합니다:

{{
  "good": ["코드 구조가 간결합니다.", "입력 처리를 적절히 했습니다."],
  "bad": ["정수 변환이 누락되었습니다.", "입력 검증이 없습니다."],
  "improved_code": "수정된 전체 코드 문자열"
}}

응답은 반드시 한국어나 영어로 작성해야 하며, 절대 중국어를 포함하지 마세요.
추가 설명, 마크다운, 문장 등은 절대 포함하지 마세요. 정확한 JSON만 출력하세요.

문제 제목: {title}
문제 설명: {description}
입력 조건: {inputRule}
출력 조건: {outputRule}
입력 예시: {inputExample}
출력 예시: {outputExample}

사용자 코드 ({codeLanguage}):
{code}
"""

def format_feedback_prompt(data: dict) -> str:
    return FEEDBACK_PROMPT.format(**data)


FEEDBACK_CHAT_PROMPT = """
너는 사용자의 코드와 문제에 대해 피드백을 주고받는 친절한 챗봇이야.
지금까지의 대화를 참고해 적절하게 응답해줘.

{history}

사용자: {user_input}
AI:
""".strip()

def format_feedback_chat_prompt(history: list[dict], user_input: str) -> str:
    # ChatML history → 텍스트로 변환
    history_text = ""
    for msg in history:
        prefix = "사용자" if msg["role"] == "user" else "AI"
        history_text += f"{prefix}: {msg['content']}\n"

    return FEEDBACK_CHAT_PROMPT.format(history=history_text.strip(), user_input=user_input.strip())


# ✅ 모의 면접 - 첫 질문
INTERVIEW_START_PROMPT = """
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
입력 조건: {inputRule}
출력 조건: {outputRule}
입력 예시: {inputExample}
출력 예시: {outputExample}

사용자 코드 ({codeLanguage}):
{code}
"""

def format_interview_start_prompt(data: dict) -> str:
    return INTERVIEW_START_PROMPT.format(**data)
