# 실행 파일 (매일 아침 10시에 실행)

# 백준 문제 크롤링 및 해설지 생성을 위한 메인 함수
import asyncio
from src.crawler.daily_crawler import get_today_workbook_id, get_problem_ids_from_workbook
from src.crawler.pipeline import crawl_generate_post
from src.crawler.boj_crawler import login_with_cookies, create_driver, crawl_boj_problem_with_selenium
from src.core.logger import setup_logging

setup_logging()

if __name__ == "__main__":
    GROUP_ID = 23567
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