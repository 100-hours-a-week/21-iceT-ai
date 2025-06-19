# 실행 파일 (매일 아침 10시에 실행)

import asyncio
import logging
from src.crawler.boj_crawler import (
    get_today_workbook_id,
    get_problem_ids_from_workbook,
    create_driver,
    login_with_cookies,
    crawl_boj_problem_with_selenium,
)
from src.crawler.boj_pipeline import crawl_generate_post

logger = logging.getLogger(__name__)


# 문제 하나 처리
async def process_one_problem(pid, driver):
    data = crawl_boj_problem_with_selenium(driver, pid)
    if not data["title"]:
        logger.warning(f"[{pid}] 문제 데이터 크롤링 실패: 제목이 비어있음")
        return

    logger.info(f"[{pid}] 문제 데이터 크롤링 성공: {data['title']}")
    logger.info(f"[{pid}] 해설 생성 및 포스팅 시작…")
    await crawl_generate_post(data)
    logger.info(f"[{pid}] 해설 생성 및 포스팅 완료")


# 여러 문제 처리
async def main_async(pids, driver):
    for pid in pids:
        await process_one_problem(pid, driver)


# 진입점
if __name__ == "__main__":
    GROUP_ID = 23567
    print ("🚀 드라이버 생성 시작")
    driver = create_driver()
    print ("✅ 드라이버 생성 완료")

    try:
        login_with_cookies(driver)
        print("🔐 로그인 완료")
        today_wb_id = get_today_workbook_id(driver)
        print(f"📘 오늘의 워크북 ID: {today_wb_id}")
        pids = get_problem_ids_from_workbook(driver, group_id=GROUP_ID, workbook_id=today_wb_id)
        print(f"📑 오늘의 문제 ID 목록: {pids}")
        asyncio.run(main_async(pids, driver))

    except Exception as e:
        logger.error(f"파이프라인 실행 중 오류 발생: {str(e)}", exc_info=True)
        raise
    finally:
        driver.quit()
