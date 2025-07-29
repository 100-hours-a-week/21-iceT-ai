from langchain_core.prompts import PromptTemplate
from src.schemas.chatbot_schema import (
    FeedbackRequest,
    FeedbackfollowRequest,
    InterviewStartRequest,
    InterviewfollowRequest,
    SummaryRequest,
)

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

# --- Feedback Start ---
def feedback_start_good_points(req: FeedbackRequest) -> str:
    """
    feedback/start 에서 '잘한 점' 에이전트를 위한 프롬프트
    """
    return f"""
문제 번호: {req.problemNumber}
제목: {req.title}

문제 설명:
{req.description}

입력 조건:
{req.inputDescription}

출력 조건:
{req.outputDescription}

입/출력 예시:
입력: {req.inputExample}
출력: {req.outputExample}

사용자 제출 코드 ({req.codeLanguage}):
```
{req.code}
```

## 잘한 점 3가지를 간결하게 알려줘.
""".strip()


def feedback_start_bad_points(req: FeedbackRequest) -> str:
    """
    feedback/start 에서 '개선할 점' 에이전트를 위한 프롬프트
    """
    return f"""
문제 번호: {req.problemNumber}
제목: {req.title}

문제 설명:
{req.description}

입력 조건:
{req.inputDescription}

출력 조건:
{req.outputDescription}

입/출력 예시:
입력: {req.inputExample}
출력: {req.outputExample}

사용자 제출 코드 ({req.codeLanguage}):
```
{req.code}
```

위 문제와 사용자의 코드를 참고하여,

## 개선할 점 3가지를 구체적으로, 그리고 왜 그렇게 생각하는지 간단한 이유를 함께 설명해줘.
""".strip()


def feedback_start_fix_code(req: FeedbackRequest, good_points: str = "", bad_points: str = "") -> str:
    """
    feedback/start 에서 '개선된 코드' 에이전트를 위한 프롬프트
    이전 에이전트들의 피드백을 참고하여 개선된 코드 생성
    """
    return f"""
문제 번호: {req.problemNumber}
제목: {req.title}

문제 설명:
{req.description}

입력 조건:
{req.inputDescription}

출력 조건:
{req.outputDescription}

입/출력 예시:
입력: {req.inputExample}
출력: {req.outputExample}

사용자 제출 코드 ({req.codeLanguage}):
```
{req.code}
```

잘한 점:
{good_points}

개선할 점:
{bad_points}

위 피드백을 반영하여, 문제를 정확히 해결하는 동일한 언어({req.codeLanguage})로 개선된 코드를 전체 구현해줘. 
반드시 문제의 입출력 조건을 만족하고, 개선할 점에서 지적된 사항들을 해결한 코드를 작성해줘.
코드 블록만 출력해줘.
""".strip()


# --- Feedback Follow-up ---
def feedback_followup(req: FeedbackfollowRequest) -> str:
    """
    feedback/answer 에서 후속 질문·요청에 대한 응답을 위한 프롬프트
    (이전 대화(req.messages)와 summary(req.summary)를 컨텍스트로 삼아
     최신 user 메시지에 답변하도록 유도)
    """
    # messages 는 시스템+사용자+어시스턴트 메시지 리스트
    # summary 가 제공되었다면 앞에 포함
    prefix = f"이전 요약: {req.summary}\n\n" if req.summary else ""
    return (
        prefix
        + "아래 대화 내역을 참고하여, 가장 최신 사용자의 요청에 정확히 답변해줘.\n\n"
        + "\n".join(f"{m.role}: {m.content}" for m in req.messages)
    )


# --- Summary ---
def summary_prompt(req: SummaryRequest) -> str:
    """
    summary 엔드포인트용 프롬프트: 문제 정보 + 대화 요약을
    하나의 긴 텍스트(문장)로 생성
    """
    convo = "\n".join(f"{m.role}: {m.content}" for m in req.messages)
    return f"""
아래 대화 및 문제 정보를 종합하여,
'문제 개요'와 '대화 흐름 요약'을 연결한 하나의 긴 텍스트 한 문장으로 작성해줘.

{convo}
""".strip()


# --- Interview: Question Batch 생성 ---
def generate_question_set_prompt(req: InterviewStartRequest, count: int = 5) -> str:
    """
    /interview/start 에서 호출.
    문제 정보와 사용자 코드를 바탕으로, count개의 주요 질문 목록을 Markdown 순서 목록으로 생성.
    """
    return f"""
문제 제목: {req.title}
설명:
{req.description}

사용자 코드 ({req.codeLanguage}):
```
{req.code}
```

→ 위 내용을 바탕으로, 다음 5가지 평가 축(문제 이해, 알고리즘 선택, 코드 품질, 테스트 설계, 커뮤니케이션)을
고루 다루는 핵심 인터뷰 질문 {count}개를 Markdown 순서 목록(1.~{count}.) 형태로 출력해주세요.
""".strip()


# --- Interview: 후속 질문 ---
def followup_prompt(prev_q: str, user_resp: str) -> str:
    """
    /interview/answer 에서, 직전 질문과 사용자의 응답을 보고
    더 깊이 파고들 후속 질문 한 개 생성.
    """
    return f"""
질문: {prev_q}
응답: {user_resp}

→ 이 답변을 바탕으로 더 깊이 탐색할 후속 질문 한 개만 출력해주세요.
""".strip()


# --- Interview: 종료 판단 ---
def finish_prompt(context: str, question_bank: list[str]) -> str:
    """
    /interview/answer 흐름 중, 전체 대화와 남은 주요 질문의 수를 보고
    인터뷰를 종료할지(True/False) 판단하도록 유도.
    """
    return f"""
[전체 대화]
{context}

[남은 주요 질문 개수]
{len(question_bank)}

→ 남은 주요 질문이 없고, 충분히 평가가 이루어졌으면 True, 아니면 False만 출력하세요.
""".strip()


# --- Interview: 최종 평가(총평) ---
def evaluation_prompt(context: str, code: str, messages: list) -> str:
    """
    인터뷰 종료 시 호출.
    문제 설명·사용자 코드·전체 대화를 종합해 Markdown 형식의 면접 총평 생성.
    """
    convo = "\n".join(f"{m.role}: {m.content}" for m in messages)
    return f"""
문제 설명 및 사용자 코드:
{code}

전체 대화 맥락:
{convo}

→ 위 내용을 종합해, Markdown으로 된 "## 📝 면접 총평"을 생성해주세요.
(세부 항목: 문제 이해, 알고리즘 선택, 코드 품질, 테스트 설계, 커뮤니케이션)
""".strip()


def should_continue_followup_prompt(messages) -> str:
    """
    대화 흐름을 보고 현재 주제에 대해 꼬리질문을 계속할지 판단하는 프롬프트
    """
    conversation = "\n".join(f"{msg.role}: {msg.content}" for msg in messages[-6:])  # 최근 6개 메시지만
    
    return f"""
당신은 코딩 면접관입니다. 아래 대화 흐름을 보고 현재 주제에 대해 꼬리질문을 계속할지 판단해주세요.

최근 대화:
{conversation}

판단 기준:
- 응답자가 충분히 깊이 있게 답변했다면 → false
- 응답자의 답변이 표면적이고 더 깊이 파고들 가치가 있다면 → true  
- 같은 주제로 이미 2-3번 이상 꼬리질문을 했다면 → false
- 응답자가 명확하고 완전한 답변을 제공했다면 → false
- 응답자가 회피하거나 불완전한 답변을 했다면 → true

오직 "true" 또는 "false"로만 답변하세요.
"""
