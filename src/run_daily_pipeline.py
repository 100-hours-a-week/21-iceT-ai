# 실행 파일 (매일 아침 10시에 실행)

# 백준 문제 크롤링 및 해설지 생성을 위한 메인 함수 
import asyncio
import logging
from src.crawler.daily_crawler import get_today_workbook_id, get_problem_ids_from_workbook
from src.crawler.boj_crawler import login_with_cookies, create_driver, crawl_boj_problem_with_selenium
from src.core.logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

async def process_one_problem(pid, driver):
    data = crawl_boj_problem_with_selenium(driver, pid)
    if not data["title"]:
        logger.warning(f"[{pid}] 문제 데이터 크롤링 실패: 제목이 비어있음")
        return

    logger.info(f"[{pid}] 문제 데이터 크롤링 성공: {data['title']}")
    logger.info(f"[{pid}] 해설 생성 및 포스팅 시작…")
    from src.crawler.pipeline import crawl_generate_post
    await crawl_generate_post(data)
    logger.info(f"[{pid}] 해설 생성 및 포스팅 완료")


async def main_async(pids, driver):
    for pid in pids:
        await process_one_problem(pid, driver)



if __name__ == "__main__":
    GROUP_ID = 23567
    driver = create_driver()

    try:
        login_with_cookies(driver)
        today_wb_id = get_today_workbook_id(driver)
        pids = get_problem_ids_from_workbook(driver, group_id=GROUP_ID, workbook_id=today_wb_id)
        asyncio.run(main_async(pids, driver))

    except Exception as e:
        logger.error(f"파이프라인 실행 중 오류 발생: {str(e)}", exc_info=True)
        raise
    finally:
        driver.quit()
