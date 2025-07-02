import logging
import asyncio
from typing import List
from src.chatbot.config import settings
from src.chatbot.adapters.v2.llm_summary import generate_summary
from src.chatbot.schemas.v2.summary_schema import SummaryRequest, SummaryResponse


logger = logging.getLogger(__name__)

# 대화 요약 서비스 함수
async def summarize_chat(requests: List[SummaryRequest]) -> List[SummaryResponse]:
    tasks = [generate_summary(r) for r in requests]
    return await asyncio.gather(*tasks)