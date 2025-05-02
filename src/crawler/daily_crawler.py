# 크롤링 코드

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


GROUP_URL = "https://www.acmicpc.net/group/workbook/23318"

def get_today_workbook_id(driver) -> int:
    """가장 최근 날짜 문제집 추출"""
    driver.get(GROUP_URL)
    try:
        row = driver.find_element(By.CSS_SELECTOR, "table tbody tr")
        link = row.find_element(By.CSS_SELECTOR, "td:nth-child(3) a")
        href = link.get_attribute("href")  
        return int(href.split("/")[-1])
    except NoSuchElementException:
        raise RuntimeError("오늘의 워크북을 찾을 수 없습니다.")


def get_problem_ids_from_workbook(driver, group_id: int, workbook_id: int) -> list[int]:
    """주어진 워크북 페이지에서 문제 번호들(ID) 추출"""
    url = f"https://www.acmicpc.net/group/workbook/view/{group_id}/{workbook_id}"
    driver.get(url)
    rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
    return [int(r.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text) for r in rows]

