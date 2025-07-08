import os
import logging
from dotenv import load_dotenv

from openai import OpenAI
from google import genai
from google.genai import types

from src.config import settings
from src.core.llm_key_manager import APIKeyManager
from src.core.stream_utils import wrap_stream_response
from src.schemas.solution_schema_v2 import SolutionResponse
from src.schemas.chatbot_schema import SummaryRequest, SummaryResponse

load_dotenv()
logger = logging.getLogger(__name__)

# --- Google Gemini (Solution) ---
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

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
        return response.parsed
    except Exception as e:
        logger.error("Gemini API 호출 실패", exc_info=True)
        raise RuntimeError("해설 생성 중 오류가 발생했습니다.") from e

# --- Upstage Solar (Interview, Feedback, Summary) ---
solar_keys = os.getenv("SOLAR_API_KEYS")
solar_key_manager = APIKeyManager(solar_keys.split(",") if solar_keys else [])

def get_solar_client():
    return OpenAI(
        api_key=solar_key_manager.next_key(),
        base_url="https://api.upstage.ai/v1"
    )

async def call_interview_agent(prompt: str, stream: bool = True, max_tokens: int = None, session_id: str = None):
    """인터뷰용 LLM 호출 (SSE 지원)"""
    max_tokens = max_tokens or settings.max_tokens_chat
    try:
        client = get_solar_client()
        response = client.chat.completions.create(
            model=settings.model_chat,
            temperature=settings.temperature_chat,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
            stream=stream
        )
        if stream:
            return wrap_stream_response(response, session_id=session_id)
        else:
            return response.choices[0].message.content
    except Exception as e:
        logger.error("Interview Agent 호출 실패", exc_info=True)
        raise RuntimeError("인터뷰 에이전트 응답 생성 실패") from e

async def call_feedback_agent(prompt: str, stream: bool = True, max_tokens: int = None, session_id: str = None):
    """피드백용 LLM 호출 (SSE 지원)"""
    max_tokens = max_tokens or settings.max_tokens_chat
    try:
        client = get_solar_client()
        response = client.chat.completions.create(
            model=settings.model_chat,
            temperature=settings.temperature_chat,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
            stream=stream
        )
        if stream:
            return wrap_stream_response(response, session_id=session_id)
        else:
            return response.choices[0].message.content
    except Exception as e:
        logger.error("Feedback LLM 호출 실패", exc_info=True)
        raise RuntimeError("Feedback 응답 생성 중 오류 발생") from e

def build_summary_messages(req: SummaryRequest) -> list:
    messages_str = "\n".join(f"{m.role}: {m.content}" for m in req.messages)
    return [
        {
            "role": "system",
            "content": (
                "당신은 문제 정보와 대화 목록을 요약하는 AI입니다.\n"
                "- 문제 요약과 대화 요약을 구분하여 하나의 긴 텍스트로 출력하세요.\n"
                "- 각 항목에는 반드시 요약된 발화 내용이 포함되어야 합니다.\n"
                f"- 문제 정보는 최대 {settings.max_summary_sentences_problem}문장, "
                f"대화 요약은 최대 {settings.max_summary_sentences_chat}문장으로 정리하세요.\n"
                "- 두 영역은 명확히 구분되며, 통합 텍스트로 구성되어야 합니다."
            )
        },
        {
            "role": "user",
            "content": f"다음은 문제 설명과 사용자/AI 간의 대화입니다:\n{messages_str}"
        }
    ]

async def generate_summary(req: SummaryRequest) -> SummaryResponse:
    """대화 요약 생성"""
    try:
        client = get_solar_client()
        messages = build_summary_messages(req)
        response = client.chat.completions.create(
            model=settings.model_chat,
            temperature=settings.temperature_chat,
            max_tokens=settings.max_tokens_summary,
            messages=messages
        )
        content = response.choices[0].message.content
        return SummaryResponse(
            sessionId=req.sessionId,
            summary=content.strip()
        )
    except Exception as e:
        logger.error("요약 생성 실패", exc_info=True)
        raise RuntimeError("대화 요약 중 오류가 발생했습니다.") from e