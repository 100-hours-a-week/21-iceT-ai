import asyncio
import logging
import httpx
import os
import json
from openai import OpenAI
from src.config import settings
from pydantic import BaseModel

from src.schemas.feedback_schema import FeedbackResponse, FeedbackAnswerResponse
from src.schemas.interview_schema import InterviewStartResponse, InterviewAnswerResponse, InterviewEndResponse
from src.schemas.solution_schema import SolutionResponse
from src.schemas.summary_schema import SummaryResponse

from src.core.llm_utils import (
    parse_feedback_response,
    parse_interview_start_response,
    parse_interview_answer_response,
    parse_interview_end_response,
    parse_solution_response,
    parse_summary_response,
    parse_feedback_answer_response,
    parse_json_from_llm_output
)

logger = logging.getLogger(__name__)

def to_messages(prompt_or_messages):
    if isinstance(prompt_or_messages, str):
        return [{"role": "user", "content": prompt_or_messages}]
    return prompt_or_messages


# ✅ 분기 방식: Upstage vs vLLM
async def generate(prompt_or_messages, schema_class, original_input=None) -> BaseModel:
    messages = to_messages(prompt_or_messages)

    if settings.use_upstage:
        # 🔶 Upstage 클라이언트
        client = OpenAI(
            api_key=settings.upstage_api_key,
            base_url="https://api.upstage.ai/v1"
        )

        # structured output 요구
        base_schema = schema_class.model_json_schema()
        core_schema = {
            "type": "object",
            "properties": base_schema["properties"],
            "required": base_schema.get("required", []),
            "additionalProperties": False
        }

        response_format = {
            "type": "json_schema",
            "json_schema": {
                "name": schema_class.__name__,
                "description": f"{schema_class.__name__} structured output",
                "strict": True,
                "schema": core_schema
            }
        }

        try:
            response = client.chat.completions.create(
                model=settings.upstage_model,
                messages=messages,
                response_format=response_format,
                temperature=settings.generation_temperature,
                max_tokens=settings.generation_max_tokens,
            )
            content = response.choices[0].message.content
            return schema_class.model_validate_json(content)
        except Exception as e:
            logger.error("Upstage 호출 실패", exc_info=True)
            raise RuntimeError("해설 생성 중 오류가 발생했습니다.") from e

    else:
        # 🔷 기존 vLLM 서버 호출
        async with httpx.AsyncClient() as client:
            response = await client.post(
                settings.vllm_url,
                json={
                    "model": settings.vllm_model,
                    "messages": messages,
                    "temperature": settings.generation_temperature,
                    "max_tokens": settings.generation_max_tokens,
                    "top_p": 0.9
                },
                timeout=120.0
            )
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            
            SCHEMA_PARSERS = {
                FeedbackResponse: lambda content, input: parse_feedback_response(content, input),
                FeedbackAnswerResponse: lambda content, input: parse_feedback_answer_response(content, input.sessionId),  # ← 이 줄 추가
                InterviewStartResponse: lambda content, input: parse_interview_start_response(content, input),
                InterviewAnswerResponse: lambda content, input: parse_interview_answer_response(content, input.sessionId),
                InterviewEndResponse: lambda content, _: parse_interview_end_response(content),
                SolutionResponse: lambda content, _: parse_solution_response(content),
                SummaryResponse: lambda content, input: parse_summary_response(content, input.sessionId),
            }

            if schema_class in SCHEMA_PARSERS:
                return SCHEMA_PARSERS[schema_class](content, original_input)
            else:
                parsed = parse_json_from_llm_output(content)
                return schema_class(**parsed)

