# src/service/chatbot_service_v3.py

from typing import Generator, List, Dict, AsyncGenerator, Optional
import re
import threading
import asyncio
import logging
import httpx
from langsmith import traceable
from src.adapters.llm_client_v3 import (
    call_feedback_agent, 
    call_interview_agent, 
    generate_summary,
    text_to_sse
)
from src.core.prompt_templates_v3 import (
    feedback_start_good_points,
    feedback_start_bad_points,
    feedback_start_fix_code,
    feedback_followup,
    summary_prompt,
    generate_question_set_prompt,
    followup_prompt,
    finish_prompt,
    evaluation_prompt,
    should_continue_followup_prompt,
    interview_evaluation_good_points,
    interview_evaluation_bad_points,
    interview_evaluation_recommendations
)
from src.schemas.chatbot_schema import (
    FeedbackRequest, FeedbackfollowRequest,
    InterviewStartRequest, InterviewfollowRequest,
    SummaryRequest, SummaryResponse
)
from src.config import BACKEND_INTERVIEW_URL

# 세션ID별 질문 뱅크 저장 (모듈 레벨)
_question_banks: Dict[str, List[str]] = {}
# 세션ID별 이전 응답 저장 (재생성 로직용)
_session_responses: Dict[str, List[str]] = {}
# 세션ID별 원본 요청 저장 (총평 생성용)
_session_requests: Dict[str, InterviewStartRequest] = {}
_lock = threading.Lock()

logger = logging.getLogger(__name__)

async def notify_interview_end(session_id: int, finished: bool):
    """인터뷰 종료 상태를 백엔드에 알리는 함수"""
    try:
        if not BACKEND_INTERVIEW_URL:
            logger.warning("[notify_interview_end] BACKEND_INTERVIEW_URL이 설정되지 않음")
            return
            
        print(f"[notify_interview_end] finished: {finished}")  # finished 상태 출력
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(
                BACKEND_INTERVIEW_URL,
                json={"sessionId": session_id, "finished": finished},
            )
            if response.status_code != 200:
                logger.warning(f"[notify_interview_end] 상태코드 {response.status_code}: {response.text}")
    except Exception as e:
        logger.warning(f"[notify_interview_end] 호출 실패: {e}")

def save_question_bank(session_id: str, questions: List[str]) -> None:
    """session_id에 대응되는 question bank를 저장합니다."""
    with _lock:
        _question_banks[session_id] = questions.copy()
        logger.info(f"[QUESTION_BANK] Session {session_id}: 질문 뱅크 저장 완료 ({len(questions)}개 질문)")
        for i, q in enumerate(questions, 1):
            logger.debug(f"[QUESTION_BANK] Session {session_id}: Q{i} - {q[:50]}...")

def pop_next_question(session_id: str) -> str:
    """session_id의 question bank에서 첫 번째 질문을 꺼내 반환합니다."""
    with _lock:
        bank = _question_banks.get(session_id)
        if not bank:
            logger.error(f"[QUESTION_BANK] Session {session_id}: 질문 뱅크가 비어있음")
            raise KeyError(f"No questions left for session {session_id}")
        next_q = bank.pop(0)
        _question_banks[session_id] = bank
        remaining_count = len(bank)
        logger.info(f"[QUESTION_BANK] Session {session_id}: 질문 팝 완료 (남은 질문: {remaining_count}개)")
        logger.debug(f"[QUESTION_BANK] Session {session_id}: 팝된 질문 - {next_q[:50]}...")
    return next_q

def has_next_question(session_id: str) -> bool:
    """session_id에 아직 남은 질문이 있는지 여부를 반환합니다."""
    with _lock:
        bank = _question_banks.get(session_id, [])
        has_questions = len(bank) > 0
        logger.debug(f"[QUESTION_BANK] Session {session_id}: 남은 질문 확인 - {len(bank)}개 ({has_questions})")
        return has_questions

def clear_question_bank(session_id: str) -> None:
    """interview 종료 시 호출하여 메모리에서 question bank를 삭제합니다."""
    with _lock:
        removed_bank = _question_banks.pop(session_id, None)
        if removed_bank:
            logger.info(f"[QUESTION_BANK] Session {session_id}: 질문 뱅크 정리 완료 ({len(removed_bank)}개 질문 삭제)")
        else:
            logger.warning(f"[QUESTION_BANK] Session {session_id}: 정리할 질문 뱅크가 없음")

def get_session_responses(session_id: str) -> List[str]:
    """세션의 이전 응답들을 가져옵니다."""
    with _lock:
        return _session_responses.get(session_id, []).copy()

def add_session_response(session_id: str, response: str) -> None:
    """세션에 새로운 응답을 추가합니다."""
    with _lock:
        if session_id not in _session_responses:
            _session_responses[session_id] = []
        _session_responses[session_id].append(response)
        # 최대 5개까지만 유지 (메모리 절약)
        if len(_session_responses[session_id]) > 5:
            _session_responses[session_id] = _session_responses[session_id][-5:]
        logger.debug(f"[SESSION_RESPONSES] Session {session_id}: 응답 추가 ({len(_session_responses[session_id])}개 저장)")

def clear_session_responses(session_id: str) -> None:
    """세션의 응답 히스토리를 정리합니다."""
    with _lock:
        removed_responses = _session_responses.pop(session_id, [])
        if removed_responses:
            logger.info(f"[SESSION_RESPONSES] Session {session_id}: 응답 히스토리 정리 완료 ({len(removed_responses)}개 응답 삭제)")
        else:
            logger.warning(f"[SESSION_RESPONSES] Session {session_id}: 정리할 응답 히스토리가 없음")

def save_original_request(session_id: str, req: InterviewStartRequest) -> None:
    """인터뷰 시작 시 원본 요청을 저장"""
    with _lock:
        _session_requests[session_id] = req
        logger.debug(f"[SESSION_REQUEST] Session {session_id}: 원본 요청 저장 완료")

def get_original_request(session_id: str) -> Optional[InterviewStartRequest]:
    """저장된 원본 요청 반환"""
    with _lock:
        return _session_requests.get(session_id)

def clear_original_request(session_id: str) -> None:
    """원본 요청 정리"""
    with _lock:
        removed_req = _session_requests.pop(session_id, None)
        if removed_req:
            logger.debug(f"[SESSION_REQUEST] Session {session_id}: 원본 요청 정리 완료")
        else:
            logger.warning(f"[SESSION_REQUEST] Session {session_id}: 정리할 원본 요청이 없음")

class ChatbotService:
    # --- Feedback ---
    # @traceable 데코레이터 제거 또는 수정
    async def start_feedback(self, req: FeedbackRequest) -> AsyncGenerator[str, None]:
        """
        feedback/start: 잘한 점, 개선할 점, 개선된 코드를
        순차적으로 생성하여 스트리밍으로 반환하는 제너레이터
        """
        session_id = str(req.sessionId)
        logger.info(f"[MULTI_AGENT] Session {session_id}: 피드백 멀티에이전트 시작")
        
        # 1) 잘한 점
        logger.info(f"[MULTI_AGENT] Session {session_id}: Agent 1/3 - 잘한 점 생성 시작")
        prompt1 = feedback_start_good_points(req)
        logger.debug(f"[MULTI_AGENT] Session {session_id}: 잘한 점 프롬프트 길이: {len(prompt1)} chars")
        good = await call_feedback_agent(prompt1, stream=False)
        logger.info(f"[MULTI_AGENT] Session {session_id}: Agent 1/3 - 잘한 점 생성 완료 ({len(str(good))} chars)")

        # 2) 개선할 점
        logger.info(f"[MULTI_AGENT] Session {session_id}: Agent 2/3 - 개선할 점 생성 시작")
        prompt2 = feedback_start_bad_points(req)
        logger.debug(f"[MULTI_AGENT] Session {session_id}: 개선할 점 프롬프트 길이: {len(prompt2)} chars")
        bad = await call_feedback_agent(prompt2, stream=False)
        logger.info(f"[MULTI_AGENT] Session {session_id}: Agent 2/3 - 개선할 점 생성 완료 ({len(str(bad))} chars)")

        # 3) 개선된 코드 - 재생성 로직 활성화
        logger.info(f"[MULTI_AGENT] Session {session_id}: Agent 3/3 - 개선된 코드 생성 시작")
        prompt3 = feedback_start_fix_code(req, str(good), str(bad))
        logger.debug(f"[MULTI_AGENT] Session {session_id}: 개선된 코드 프롬프트 길이: {len(prompt3)} chars")
        
        # 이전 응답들을 가져와서 재생성 로직에 사용
        prev_responses = get_session_responses(session_id)
        logger.debug(f"[MULTI_AGENT] Session {session_id}: 이전 응답 {len(prev_responses)}개 로드됨")
        
        fixed_code = await call_feedback_agent(
            prompt3, 
            stream=False, 
            session_id=session_id, 
            endpoint="feedback-fix-code",
            prev_responses=prev_responses
        )
        
        # 생성된 응답을 세션에 저장
        add_session_response(session_id, str(fixed_code))
        logger.info(f"[MULTI_AGENT] Session {session_id}: Agent 3/3 - 개선된 코드 생성 완료 ({len(str(fixed_code))} chars)")

        # 마크다운 헤더·본문·코드블록을 한꺼번에 조립
        full_md = (
            f"## 👍 잘한 점\n\n{good}\n\n"
            f"## 👎 개선할 점\n\n{bad}\n\n"
            f"## 🛠️ 개선된 코드\n\n{fixed_code}"
        )
        
        logger.info(f"[MULTI_AGENT] Session {session_id}: 피드백 멀티에이전트 완료 - 최종 마크다운 ({len(full_md)} chars)")
        
        # 단어 단위 청킹 + 줄바꿈 이벤트로 streaming
        chunk_count = 0
        for chunk in text_to_sse(full_md, chunk_size=1):
            chunk_count += 1
            yield chunk
        
        logger.debug(f"[MULTI_AGENT] Session {session_id}: 스트리밍 완료 ({chunk_count}개 청크)")

    # @traceable 데코레이터 제거 또는 수정  
    async def followup_feedback(self, req: FeedbackfollowRequest) -> AsyncGenerator[str, None]:
        """
        feedback/answer: 후속 요청에 대해
        단일 에이전트로 답변을 스트리밍으로 반환
        """
        prompt = feedback_followup(req)
        
        try:
            response_generator = await call_feedback_agent(
                prompt, 
                stream=True,
                session_id=str(req.sessionId) if hasattr(req, 'sessionId') else None,
                endpoint="feedback-answer"
            )
            
            # 디버깅: 반환된 객체의 타입 확인
            logger.debug(f"[FOLLOWUP_FEEDBACK] response_generator type: {type(response_generator)}")
            logger.debug(f"[FOLLOWUP_FEEDBACK] has __anext__: {hasattr(response_generator, '__anext__')}")
            logger.debug(f"[FOLLOWUP_FEEDBACK] has __aiter__: {hasattr(response_generator, '__aiter__')}")
            
            # AsyncGenerator 처리를 try-except로 안전하게 처리
            try:
                # AsyncGenerator라고 가정하고 시도
                logger.debug("[FOLLOWUP_FEEDBACK] Attempting AsyncGenerator processing")
                async for chunk in response_generator:  # type: ignore
                    yield chunk
            except (TypeError, AttributeError) as e:
                # AsyncGenerator가 아닌 경우 (str 등)
                logger.debug(f"[FOLLOWUP_FEEDBACK] Not AsyncGenerator, processing as string: {e}")
                text_content = str(response_generator)
                for chunk in text_to_sse(text_content):
                    yield chunk
                    
        except Exception as e:
            logger.error(f"[FOLLOWUP_FEEDBACK] 전체 에러 발생: {str(e)}", exc_info=True)
            # 에러 발생 시 대체 메시지
            fallback_msg = "죄송합니다. 답변 생성 중 오류가 발생했습니다."
            for chunk in text_to_sse(fallback_msg):
                yield chunk

    # --- Interview ---
    # @traceable 데코레이터 제거 또는 수정
    async def start_interview(self, req: InterviewStartRequest) -> AsyncGenerator[str, None]:
        """
        1) 문제 정보 + 사용자 코드로 질문 셋 생성
        2) Markdown 리스트 파싱 → question_bank 저장
        3) 첫 번째 질문 pop → SSE로 스트리밍
        """
        session_id = str(req.sessionId)
        logger.info(f"[INTERVIEW_FLOW] Session {session_id}: 인터뷰 시작 - 문제 {req.problemNumber}")
        
        # 1) Prompt 만들기
        question_prompt = generate_question_set_prompt(req, count=5)
        logger.debug(f"[INTERVIEW_FLOW] Session {session_id}: 질문 생성 프롬프트 길이: {len(question_prompt)} chars")

        # 2) LLM 호출 (Markdown 순서 목록 반환)
        logger.info(f"[INTERVIEW_FLOW] Session {session_id}: LLM 호출하여 질문 셋 생성 중...")
        questions_md = await call_interview_agent(
            question_prompt, 
            stream=False,
            session_id=session_id,
            endpoint="interview-start"
        )
        logger.info(f"[INTERVIEW_FLOW] Session {session_id}: 질문 셋 생성 완료 ({len(str(questions_md))} chars)")

        # 3) Markdown 목록 파싱 함수 (예: "1. 질문 내용" → "질문 내용")
        def parse_markdown_list(md: str) -> List[str]:
            items: List[str] = []
            for line in str(md).splitlines():
                m = re.match(r'^\s*\d+\.\s*(.+)$', line)
                if m:
                    items.append(m.group(1).strip())
            logger.debug(f"[INTERVIEW_FLOW] Session {session_id}: 파싱된 질문 항목: {len(items)}개")
            return items

        questions = parse_markdown_list(str(questions_md))
        logger.info(f"[INTERVIEW_FLOW] Session {session_id}: 마크다운 파싱 완료 - {len(questions)}개 질문 추출")

        # 4) in-memory question_bank 저장
        save_question_bank(session_id, questions)
        
        # 원본 요청도 저장 (총평 생성용)
        save_original_request(session_id, req)

        # 5) 첫 질문 꺼내기
        try:
            first_q = pop_next_question(session_id)
            logger.info(f"[INTERVIEW_FLOW] Session {session_id}: 첫 번째 질문 선택 완료")
        except KeyError:
            # 혹시 질문이 하나도 안나왔을 때 대비
            first_q = "죄송합니다. 질문을 생성하는 데 문제가 발생했습니다."
            logger.error(f"[INTERVIEW_FLOW] Session {session_id}: 질문 뱅크가 비어있어 대체 메시지 사용")

        # 6) SSE word-level 청킹으로 스트리밍
        # 인터뷰 시작 상태 전송
        asyncio.create_task(notify_interview_end(int(session_id), finished=False))
        chunk_count = 0
        for chunk in text_to_sse(first_q):
            chunk_count += 1
            yield chunk
        
        logger.info(f"[INTERVIEW_FLOW] Session {session_id}: 첫 번째 질문 스트리밍 완료 ({chunk_count}개 청크)")

    # @traceable 데코레이터 제거 또는 수정
    async def followup_interview(self, req: InterviewfollowRequest) -> AsyncGenerator[str, None]:
        """
        interview/answer: 
        클라이언트로부터 받은 최신 메시지 + 최근 10개 이전 메시지 + 요약문을 활용
        """
        session_id = str(req.sessionId)
        logger.info(f"[INTERVIEW_FLOW] Session {session_id}: 인터뷰 후속 처리 시작")
        
        # 최근 10개 메시지만 사용 (메모리 효율성)
        recent_messages = req.messages[-10:] if len(req.messages) > 10 else req.messages
        
        # 1) 대화 문맥 조합 (요약문 + 최근 메시지들)
        summary_context = f"이전 대화 요약: {req.summary}\n\n" if hasattr(req, 'summary') and req.summary else ""
        context = summary_context + "\n".join(f"{m.role}: {m.content}" for m in recent_messages)
        
        # 2) LLM이 꼬리질문을 계속할지 판단 (최근 6개만 사용)
        should_continue_prompt = should_continue_followup_prompt(recent_messages[-6:])
        should_continue = await call_interview_agent(
            should_continue_prompt, 
            stream=False,
            session_id=session_id,
            endpoint="interview-decision"
        )
        
        # 3) 꼬리질문 계속하기로 판단했다면
        if str(should_continue).strip().lower() == "true":
            logger.info(f"[INTERVIEW_FLOW] Session {session_id}: 꼬리질문 계속 진행")
            prev_q = req.messages[-2].content if len(req.messages) >= 2 else ""
            last_resp = req.messages[-1].content
            tail_q_prompt = followup_prompt(prev_q, last_resp)
            tail_q = await call_interview_agent(
                tail_q_prompt, 
                stream=False,
                session_id=session_id,
                endpoint="interview-followup"
            )
            
            if str(tail_q).strip():
                # 인터뷰 진행 상태 전송
                asyncio.create_task(notify_interview_end(int(session_id), finished=False))
                for chunk in text_to_sse(str(tail_q)):
                    yield chunk
                return

        # 4) 꼬리질문 중단 → 다음 주요 질문으로
        if has_next_question(session_id):
            logger.info(f"[INTERVIEW_FLOW] Session {session_id}: 다음 주요 질문으로 이동")
            next_q = pop_next_question(session_id)
            # 인터뷰 진행 상태 전송
            asyncio.create_task(notify_interview_end(int(session_id), finished=False))
            for chunk in text_to_sse(next_q):
                yield chunk
            return

        # 5) 질문 모두 소진 → 종료 판단
        logger.info(f"[INTERVIEW_FLOW] Session {session_id}: 모든 질문 소진 - 종료 판단 중")
        finish_decision_prompt = finish_prompt(context, [])
        decision = await call_interview_agent(
            finish_decision_prompt,
            stream=False,
            session_id=session_id,
            endpoint="interview-finish"
        )
        
        if str(decision).strip().lower() == "true":
            # 6) 총평 생성 - 멀티 에이전트 방식
            logger.info(f"[INTERVIEW_FLOW] Session {session_id}: 인터뷰 종료 - 총평 생성 중")
            
            original_req = get_original_request(session_id)
            if original_req:
                # 1) 잘한 점 생성
                logger.info(f"[INTERVIEW_EVALUATION] Session {session_id}: Agent 1/3 - 잘한 점 생성 시작")
                good_prompt = interview_evaluation_good_points(original_req, req.messages)
                good_points = await call_interview_agent(
                    good_prompt,
                    stream=False,
                    session_id=session_id,
                    endpoint="interview-evaluation-good"
                )
                logger.info(f"[INTERVIEW_EVALUATION] Session {session_id}: Agent 1/3 - 잘한 점 생성 완료")

                # 2) 개선할 점 생성
                logger.info(f"[INTERVIEW_EVALUATION] Session {session_id}: Agent 2/3 - 개선할 점 생성 시작")
                bad_prompt = interview_evaluation_bad_points(original_req, req.messages)
                bad_points = await call_interview_agent(
                    bad_prompt,
                    stream=False,
                    session_id=session_id,
                    endpoint="interview-evaluation-bad"
                )
                logger.info(f"[INTERVIEW_EVALUATION] Session {session_id}: Agent 2/3 - 개선할 점 생성 완료")

                # 3) 학습 추천사항 생성
                logger.info(f"[INTERVIEW_EVALUATION] Session {session_id}: Agent 3/3 - 학습 추천사항 생성 시작")
                rec_prompt = interview_evaluation_recommendations(original_req, req.messages, str(good_points), str(bad_points))
                recommendations = await call_interview_agent(
                    rec_prompt,
                    stream=False,
                    session_id=session_id,
                    endpoint="interview-evaluation-recommendations"
                )
                logger.info(f"[INTERVIEW_EVALUATION] Session {session_id}: Agent 3/3 - 학습 추천사항 생성 완료")

                # 4) 마크다운 형식으로 조합
                full_evaluation = (
                    f"## 📝 면접 총평\n\n"
                    f"### 👍 잘한 점\n\n{good_points}\n\n"
                    f"### 👎 개선할 점\n\n{bad_points}\n\n"
                    f"### 📚 학습 추천사항\n\n{recommendations}"
                )
                
                logger.info(f"[INTERVIEW_EVALUATION] Session {session_id}: 총평 완료 - 마크다운 ({len(full_evaluation)} chars)")
                
                # 5) SSE 스트리밍으로 반환
                for chunk in text_to_sse(full_evaluation):
                    yield chunk
                    
                # 인터뷰 종료 신호 전송
                asyncio.create_task(notify_interview_end(int(session_id), finished=True))
                    
                # 정리
                clear_question_bank(session_id)
                clear_original_request(session_id)
            else:
                logger.error(f"[INTERVIEW_FLOW] Session {session_id}: 원본 요청을 찾을 수 없음")
                fallback = "## 📝 면접 총평\n\n죄송합니다. 총평 생성 중 오류가 발생했습니다."
                for chunk in text_to_sse(fallback):
                    yield chunk
                # 인터뷰 종료 신호 전송 (오류 상황에서도)
                asyncio.create_task(notify_interview_end(int(session_id), finished=True))
        else:
            # 7) 재생성 또는 예외 처리
            logger.warning(f"[INTERVIEW_FLOW] Session {session_id}: 예상치 못한 상황 - 대체 메시지 반환")
            fallback = "죄송합니다. 추가 질문을 생성하는 데 문제가 발생했습니다."
            for chunk in text_to_sse(fallback):
                yield chunk

    # --- Summary ---
    @traceable(run_type="chain", name="summary_endpoint", tags=["summary", "conversation"])
    async def summarize(self, req: SummaryRequest) -> SummaryResponse:
        """
        summary: 단일 응답으로 문제 정보 + 대화 흐름 요약을 반환
        """
        session_id = req.sessionId
        logger.info(f"[SUMMARY_FLOW] Session {session_id}: 요약 요청 시작 - {len(req.messages)}개 메시지")
        
        result = await generate_summary(req)
        
        logger.info(f"[SUMMARY_FLOW] Session {session_id}: 요약 완료 - {len(result.summary)} chars")
        return result

    # 동기 wrapper 메서드들 (기존 호환성 유지)
    def start_feedback_sync(self, req: FeedbackRequest) -> Generator[str, None, None]:
        """동기 버전의 start_feedback - AsyncGenerator를 Generator로 변환"""
        async def async_wrapper():
            async for chunk in self.start_feedback(req):
                yield chunk
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            # AsyncGenerator를 동기적으로 실행
            gen = async_wrapper()
            while True:
                try:
                    chunk = loop.run_until_complete(gen.__anext__())
                    yield chunk
                except StopAsyncIteration:
                    break
        finally:
            loop.close()

    def followup_feedback_sync(self, req: FeedbackfollowRequest) -> Generator[str, None, None]:
        """동기 버전의 followup_feedback - AsyncGenerator를 Generator로 변환"""
        async def async_wrapper():
            async for chunk in self.followup_feedback(req):
                yield chunk
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            gen = async_wrapper()
            while True:
                try:
                    chunk = loop.run_until_complete(gen.__anext__())
                    yield chunk
                except StopAsyncIteration:
                    break
        finally:
            loop.close()

    def start_interview_sync(self, req: InterviewStartRequest) -> Generator[str, None, None]:
        """동기 버전의 start_interview - AsyncGenerator를 Generator로 변환"""
        async def async_wrapper():
            async for chunk in self.start_interview(req):
                yield chunk
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            gen = async_wrapper()
            while True:
                try:
                    chunk = loop.run_until_complete(gen.__anext__())
                    yield chunk
                except StopAsyncIteration:
                    break
        finally:
            loop.close()

    def followup_interview_sync(self, req: InterviewfollowRequest) -> Generator[str, None, None]:
        """동기 버전의 followup_interview - AsyncGenerator를 Generator로 변환"""
        async def async_wrapper():
            async for chunk in self.followup_interview(req):
                yield chunk
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            gen = async_wrapper()
            while True:
                try:
                    chunk = loop.run_until_complete(gen.__anext__())
                    yield chunk
                except StopAsyncIteration:
                    break
        finally:
            loop.close()

    def summarize_sync(self, req: SummaryRequest) -> SummaryResponse:
        """동기 버전의 summarize"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(self.summarize(req))
        finally:
            loop.close()
