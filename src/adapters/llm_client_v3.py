import os
import logging
from typing import Generator, List, Optional, Tuple
from dotenv import load_dotenv
from langsmith import traceable
import re
from google import genai
from google.genai import types
from openai import OpenAI

from src.config import settings
from src.schemas.solution_schema_v2 import SolutionResponse
from src.schemas.chatbot_schema import SummaryRequest, SummaryResponse

load_dotenv()
logger = logging.getLogger(__name__)

# --- Google Gemini (Solution) ---
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@traceable(run_type="llm")
def generate_solution(prompt_text: str) -> SolutionResponse:
    """Gemini 기반 해설 생성"""
    try:
        response = gemini_client.models.generate_content(
            model=settings.model_solution,
            contents=prompt_text,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=SolutionResponse,
                temperature=settings.temperature_solution,
                max_output_tokens=settings.max_tokens_solution,
            ),
        )
        
        # 타입 체크 및 반환
        parsed_response = response.parsed
        if parsed_response is None:
            logger.error("Parsed response is None")
            raise ValueError("Failed to parse response")
        
        # SolutionResponse 타입으로 캐스팅
        return parsed_response  # type: ignore
    except Exception as e:
        logger.error("Gemini API 호출 실패", exc_info=True)
        raise RuntimeError("해설 생성 중 오류가 발생했습니다.") from e

# --- OpenAI ChatGPT Client for chatbot functions ---
chatbot_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# SSE 유틸리티 함수
def chunk_text_words(text: str, chunk_size: int = 1) -> Generator[str, None, None]:
    """
    전체 텍스트를 단어 단위로 잘라서, chunk_size개 단어씩 묶어 반환합니다.
    """
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield " ".join(words[i : i + chunk_size])

def text_to_sse(text: str, chunk_size: int = 1) -> Generator[str, None, None]:
    """
    단어 단위로 SSE(data: <chunk>\n\n)으로 wrap하여 반환하는 제너레이터입니다.
    """
    # 단어와 공백/줄바꿈을 모두 유지하면서 분할
    tokens = re.findall(r'\S+|\s+', text)
    
    for i in range(0, len(tokens), chunk_size):
        chunk = ''.join(tokens[i:i + chunk_size])
        # 줄바꿈이 있는 경우 data: \n으로 출력
        if '\n' in chunk:
            # 줄바꿈을 포함한 청크를 처리
            parts = chunk.split('\n')
            for j, part in enumerate(parts):
                if j > 0:  # 첫 번째가 아닌 경우 줄바꿈 먼저 출력
                    yield "data: \\n\n\n"
                if part.strip():  # 빈 문자열이 아닌 경우만 출력
                    yield f"data: {part}\n\n"
        else:
            yield f"data: {chunk}\n\n"

# --- 결정자 에이전트 기반 검증 및 반려 사유 생성 ---
def llm_validate_response(new_response: str, prev_responses: Optional[List[str]], user_request: str) -> Tuple[bool, str]:
    """
    LLM을 이용해 새 응답이 이전 응답들과 너무 유사하거나, 사용자 요청과 동떨어진지 판단.
    검증 실패 시 반려 사유를 동적으로 생성.
    """
    prev_text = "\n---\n".join(prev_responses) if prev_responses else "(없음)"
    prompt = f"""
다음은 새로 생성된 응답입니다:
{new_response}

이전 응답들:
{prev_text}

사용자 요청:
{user_request}

위 새 응답이 이전 응답들과 너무 유사하거나, 사용자 요청과 동떨어진 동문서답이라면 '반려'로 판단하고, 그 이유를 한 문장으로 설명해줘. 적합하다면 '통과'라고만 답해줘.
"""
    
    logger.debug(f"[LLM_VALIDATION] 검증 프롬프트 생성 - 길이: {len(prompt)} chars")
    
    try:
        resp = chatbot_client.chat.completions.create(
            model=getattr(settings, 'model_name', 'gpt-4'),
            messages=[{"role": "user", "content": prompt}],
            stream=False,
            timeout=getattr(settings, 'timeout_seconds', 30),
        )
        judge = (resp.choices[0].message.content or "").strip()
        
        logger.debug(f"[LLM_VALIDATION] 검증 결과: '{judge}'")
        
        if judge == "통과":
            logger.info(f"[LLM_VALIDATION] 응답 검증 성공 - 품질 기준 충족")
            return True, ""
        else:
            logger.warning(f"[LLM_VALIDATION] 응답 검증 실패 - 사유: {judge}")
            return False, judge
            
    except Exception as e:
        logger.error(f"[LLM_VALIDATION] 검증 중 오류 발생: {str(e)} - 기본 통과 처리")
        return True, ""  # 검증 실패 시 기본적으로 통과 처리

# 반려 사유를 포함해 재생성 프롬프트 생성
def regenerate_with_reason(original_prompt: str, reason: str) -> str:
    return f"""
{original_prompt}

이전 응답이 반료된 이유: {reason}
위 반료 사유를 참고하여, 더 적합한 응답을 생성해줘.
"""

# LLM 호출 (비동기/동기)
@traceable(run_type="llm", name="llm_call_with_validation", tags=["llm", "validation"])
def call_llm(prompt: str, prev_responses: Optional[List[str]] = None, user_request: str = "") -> str:
    """
    Non-streaming 호출: 전체 응답을 한 번에 받아옵니다.
    결정자 에이전트(LLM)로 이전 응답들과 비교 및 동문서답 여부 판단.
    검증 실패 시 반료 사유를 생성하여 재생성 프롬프트로 재시도.
    """
    max_retry = 3
    last_result = ""
    responses = prev_responses.copy() if prev_responses else []
    
    logger.info(f"[LLM_CALL] 호출 시작 - 프롬프트 길이: {len(prompt)} chars, 이전 응답: {len(responses)}개")
    
    for attempt in range(max_retry):
        logger.info(f"[LLM_CALL] 시도 {attempt + 1}/{max_retry} - OpenAI API 호출 중...")
        
        try:
            resp = chatbot_client.chat.completions.create(
                model=getattr(settings, 'model_name', 'gpt-3.5-turbo'),
                messages=[{"role": "user", "content": prompt}],
                stream=False,
                timeout=getattr(settings, 'timeout_seconds', 30),
            )
            result = resp.choices[0].message.content or ""
            last_result = result
            
            logger.info(f"[LLM_CALL] 시도 {attempt + 1} 응답 생성 완료 - 길이: {len(result)} chars")
            
            # 결정자 에이전트로 검증
            logger.debug(f"[LLM_VALIDATION] 응답 검증 시작 - 이전 응답과 비교 중...")
            valid, reason = llm_validate_response(result, responses, user_request)
            
            if valid:
                logger.info(f"[LLM_VALIDATION] 검증 통과 - 최종 응답 반환")
                return result
            else:
                logger.warning(f"[LLM_VALIDATION] 검증 실패 (시도 {attempt + 1}) - 사유: {reason}")
                prompt = regenerate_with_reason(prompt, reason)
                responses.append(result)
                logger.info(f"[LLM_CALL] 재생성 프롬프트 준비 완료 - 길이: {len(prompt)} chars")
                
        except Exception as e:
            logger.error(f"[LLM_CALL] 시도 {attempt + 1} 실패 - 오류: {str(e)}")
            if attempt == max_retry - 1:
                raise
    
    logger.warning(f"[LLM_CALL] 최대 재시도 횟수 도달 - 마지막 결과 반환 ({len(last_result)} chars)")
    return last_result

# --- 인터뷰/피드백/요약 함수들 ---
@traceable(run_type="chain", name="interview_agent_call", tags=["interview", "chatbot"])
async def call_interview_agent(prompt: str, stream: bool = True, max_tokens: Optional[int] = None, session_id: Optional[str] = None, endpoint: str = "interview-answer"):
    """
    인터뷰 에이전트 호출 - stream 여부에 따라 응답 형태 선택
    """
    logger.info(f"[INTERVIEW_AGENT] 호출 시작 - endpoint: {endpoint}, session: {session_id}, stream: {stream}")
    
    try:
        full_text = call_llm(prompt, prev_responses=None, user_request=prompt)
        
        if stream:
            logger.info(f"[INTERVIEW_AGENT] 스트리밍 모드 - SSE 변환 시작")
            # SSE 형태로 단어 단위 청킹하여 Generator 반환
            return text_to_sse(full_text, chunk_size=1)
        else:
            logger.info(f"[INTERVIEW_AGENT] 일반 모드 - 전체 텍스트 반환 ({len(full_text)} chars)")
            # 전체 텍스트 그대로 반환
            return full_text
    except Exception as e:
        logger.error(f"[INTERVIEW_AGENT] 호출 실패 - endpoint: {endpoint}, 오류: {str(e)}", exc_info=True)
        raise RuntimeError("인터뷰 에이전트 응답 생성 실패") from e

@traceable(run_type="chain", name="feedback_agent_call", tags=["feedback", "chatbot"])
async def call_feedback_agent(prompt: str, stream: bool = True, max_tokens: Optional[int] = None, session_id: Optional[str] = None, endpoint: str = "feedback-answer"):
    """
    피드백 에이전트 호출 - stream 여부에 따라 응답 형태 선택
    """
    logger.info(f"[FEEDBACK_AGENT] 호출 시작 - endpoint: {endpoint}, session: {session_id}, stream: {stream}")
    
    try:
        full_text = call_llm(prompt, prev_responses=None, user_request=prompt)
        
        if stream:
            logger.info(f"[FEEDBACK_AGENT] 스트리밍 모드 - SSE 변환 시작")
            # SSE 형태로 단어 단위 청킹하여 Generator 반환
            return text_to_sse(full_text, chunk_size=1)
        else:
            logger.info(f"[FEEDBACK_AGENT] 일반 모드 - 전체 텍스트 반환 ({len(full_text)} chars)")
            # 전체 텍스트 그대로 반환
            return full_text
    except Exception as e:
        logger.error(f"[FEEDBACK_AGENT] 호출 실패 - endpoint: {endpoint}, 오류: {str(e)}", exc_info=True)
        raise RuntimeError("Feedback 응답 생성 중 오류 발생") from e

def build_summary_messages(req: SummaryRequest) -> str:
    messages_str = "\n".join(f"{m.role}: {m.content}" for m in req.messages)
    system_prompt = (
        "당신은 문제 정보와 대화 목록을 요약하는 AI입니다.\n"
        "- 문제 요약과 대화 요약을 구분하여 하나의 긴 텍스트로 출력하세요.\n"
        "- 각 항목에는 반드시 요약된 발화 내용이 포함되어야 합니다.\n"
        f"- 문제 정보는 최대 {getattr(settings, 'max_summary_sentences_problem', 3)}문장, "
        f"대화 요약은 최대 {getattr(settings, 'max_summary_sentences_chat', 5)}문장으로 정리하세요.\n"
        "- 두 영역은 명확히 구분되며, 통합 텍스트로 구성되어야 합니다."
    )
    return f"{system_prompt}\n\n다음은 문제 설명과 사용자/AI 간의 대화입니다:\n{messages_str}"

@traceable(run_type="chain", name="summary_generation", tags=["summary", "chatbot"])
async def generate_summary(req: SummaryRequest) -> SummaryResponse:
    """요약 생성"""
    session_id = req.sessionId
    logger.info(f"[SUMMARY_AGENT] Session {session_id}: 요약 생성 시작 - {len(req.messages)}개 메시지")
    
    try:
        prompt = build_summary_messages(req)
        logger.debug(f"[SUMMARY_AGENT] Session {session_id}: 요약 프롬프트 생성 완료 ({len(prompt)} chars)")
        
        summary_text = call_llm(prompt, prev_responses=None, user_request="요약 생성")
        
        logger.info(f"[SUMMARY_AGENT] Session {session_id}: 요약 생성 완료 ({len(summary_text)} chars)")
        
        return SummaryResponse(
            sessionId=req.sessionId,
            summary=summary_text.strip()
        )
    except Exception as e:
        logger.error(f"[SUMMARY_AGENT] Session {session_id}: 요약 생성 실패 - {str(e)}", exc_info=True)
        raise RuntimeError("대화 요약 중 오류가 발생했습니다.") from e
