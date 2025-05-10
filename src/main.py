<<<<<<< HEAD
from fastapi import FastAPI
from src.core.logger import setup_logging
from src.core.exception_handlers import add_exception_handlers

# ✅ 기능별 라우터
from src.routers.v1.solution_router import router as solution_router  # 해설 기능
from src.routers.v2.feedback_router import router as feedback_router  # 코드 피드백 챗봇
from src.routers.v2.interview_router import router as interview_router  # 모의 면접 챗봇

# ✅ 로그 및 예외 설정
setup_logging()

app = FastAPI(
    title="코딩테스트 도우미 서비스",
    version="2.0.0",
)

# ✅ 공통 예외 핸들러 등록
add_exception_handlers(app)

# ✅ 라우터 등록
app.include_router(solution_router, prefix="/api/v1", tags=["해설지 생성 기능"])
app.include_router(feedback_router, prefix="/api/v2", tags=["코드 피드백 챗봇"])
app.include_router(interview_router, prefix="/api/v2", tags=["모의 면접 챗봇"])

# ✅ 헬스체크
@app.get("/healthz")
def healthz():
    return {"status": "ok"}
=======
# from fastapi import FastAPI
# from src.core.logger import setup_logging
# from src.core.exception_handlers import add_exception_handlers
# from src.routers.v1.solution_router import router as solution_router

# # 로깅 설정 초기화
# setup_logging()

# # FastAPI 애플리케이션 생성
# app = FastAPI(
#     title="코딩테스트 도우미 서비스",
#     version="1.0.0",
# )

# # 예외 핸들러 등록
# add_exception_handlers(app)

# # API v1 라우터 등록
# app.include_router(
#     solution_router,
#     prefix="/api/ai/v1",
#     tags=["해설지 생성 기능"],
# )

# # health check 엔드포인트
# @app.get("/healthz")
# def healthz():
#     return {"status": "ok"}

import asyncio
from src.crawler.daily_crawler import get_today_workbook_id, get_problem_ids_from_workbook
from src.crawler.pipeline import crawl_generate_post
from src.crawler.boj_crawler import login_with_cookies, create_driver, crawl_boj_problem_with_selenium

if __name__ == "__main__":
    GROUP_ID = 23318
    driver = create_driver()

    try:
        login_with_cookies(driver) 
        today_wb_id = get_today_workbook_id(driver)
        print(f"오늘 워크북 ID: {today_wb_id}")

        pids = get_problem_ids_from_workbook(driver, group_id=GROUP_ID, workbook_id=today_wb_id)
        print(f"오늘 문제 ID들: {pids}")
        for pid in pids:
            print(f"[{pid}] 크롤링 중...")
            data = crawl_boj_problem_with_selenium(driver, pid)
            print(f"[{data}] 문제 데이터")
            if data["title"]:
                asyncio.run(crawl_generate_post(data))
    finally:
        driver.quit() 
>>>>>>> origin/dev
