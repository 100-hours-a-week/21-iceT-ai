import os
import logging
from dotenv import load_dotenv
from langsmith import traceable
from google import genai
from google.genai import types
import re

from src.config import settings
from src.schemas.solution_schema_v2 import SolutionResponse
from src.schemas.chatbot_schema import SummaryRequest, SummaryResponse

from src.adapters.model_loader import tokenizer, llm, sampling_params

load_dotenv()
logger = logging.getLogger(__name__)

# Gemini 기반 해설 생성

gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@traceable(run_type="llm", name="solution-mode", tags=["solution", "gemini"])
def generate_solution(prompt_text: str) -> SolutionResponse:
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

# Qwen용 공통 프롬프트 빌더

SYSTEM_MESSAGE = (
    "You are a kind and friendly chatbot for announcements who responds based on "
    "the previous conversation flow. Always answer in Korean."
)

def build_prompt(user_input: str, context: str = "") -> str:
    full_content = f"{context}\n\n{user_input}" if context else user_input
    messages = [
        {"role": "system", "content": SYSTEM_MESSAGE},
        {"role": "user", "content": full_content}
    ]
    return tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False
    )

async def extract_final_text(agen) -> str:
    last_text = ""
    async for result in agen:
        if result.outputs and result.outputs[0].text:
            last_text = result.outputs[0].text
    return last_text if last_text else "empty"

# 인터뷰 에이전트 (Qwen 기반)

@traceable(run_type="llm", name="interview-mode", tags=["interview", "qwen"])
async def call_interview_agent(
    prompt: str,
    stream: bool = True,
    max_tokens: int = None,
    session_id: str = None
):
    prompt_str = build_prompt(prompt)
    request_id = f"interview_{session_id or os.urandom(6).hex()}"
    agen = llm.generate(prompt_str, sampling_params, request_id=request_id)

    if stream:
        return stream_qwen_response(prompt, session_id=session_id)
    return await extract_final_text(agen)

# 피드백 에이전트 (Qwen 기반)

@traceable(run_type="llm", name="feedback-mode", tags=["feedback", "qwen"])
async def call_feedback_agent(
    prompt: str,
    stream: bool = True,
    max_tokens: int = None,
    session_id: str = None
):
    prompt_str = build_prompt(prompt)
    request_id = f"feedback_{session_id or os.urandom(6).hex()}"
    agen = llm.generate(prompt_str, sampling_params, request_id=request_id)

    if stream:
        return stream_qwen_response(prompt, session_id=session_id)
    return await extract_final_text(agen)

# 요약 생성 (Qwen 기반)

@traceable(run_type="llm", name="summary-mode", tags=["summary", "qwen"])
async def generate_summary(req: SummaryRequest) -> SummaryResponse:
    try:
        messages_str = "\n".join(f"{m.role}: {m.content}" for m in req.messages)
        prompt_str = build_prompt(messages_str)
        request_id = f"summary_{req.sessionId or os.urandom(6).hex()}"
        agen = llm.generate(prompt_str, sampling_params, request_id=request_id)
        summary_text = await extract_final_text(agen)
        return SummaryResponse(sessionId=req.sessionId, summary=summary_text.strip())
    except Exception as e:
        logger.error("요약 생성 실패", exc_info=True)
        raise RuntimeError("대화 요약 중 오류가 발생했습니다.") from e

# Qwen 스트리밍 응답을 직접 처리하는 async generator 함수
async def stream_qwen_response(prompt: str, session_id: str = None):
    """
    Qwen LLM의 스트리밍 응답을 단어 단위로 yield하는 async generator.
    """
    prompt_str = build_prompt(prompt)
    request_id = f"stream_{session_id or os.urandom(6).hex()}"
    agen = llm.generate(prompt_str, sampling_params, request_id=request_id)
    sent_text = ""
    async for result in agen:
        if result.outputs and result.outputs[0].text:
            text = result.outputs[0].text
            new_text = text[len(sent_text):]
            sent_text = text
            # 단어 단위로 yield
            for word in re.findall(r'\s+|\S+', new_text):
                yield word
