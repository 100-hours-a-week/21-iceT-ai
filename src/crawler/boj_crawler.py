import os
import time
import random
import platform
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.config import settings

GROUP_URL = "https://www.acmicpc.net/group/workbook/23567"

# ✅ 셀레니움 드라이버 생성
def create_driver():
    options = Options()
    
    system = platform.system().lower()
    if "windows" in system:
        chromedriver_path = "C:/Workspace/21-iceT-ai/src/crawler/chromedriver.exe"
        service = Service(chromedriver_path)

    else:
        options.binary_location = "/home/ubuntu/chrome/chrome-linux64/chrome"
        chromedriver_path = "/home/ubuntu/chrome/chromedriver-linux64/chromedriver"
        service = Service(chromedriver_path)

    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.6312.105 Safari/537.36"
    )

    driver = webdriver.Chrome(service=service, options=options)

    # 봇 탐지 우회
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', { get: () => undefined })"
    })

    return driver


# ✅ 로그인 쿠키 추가
def login_with_cookies(driver):
    driver.get("https://www.acmicpc.net/")
    driver.add_cookie({
        'name': 'OnlineJudge',
        'value': settings.boj_cookie_onlinejudge,
        'domain': '.acmicpc.net',
        'path': '/',
        'httpOnly': True,
        'secure': True
    })
    driver.add_cookie({
        'name': 'bojautologin',
        'value': settings.boj_cookie_autologin,
        'domain': '.acmicpc.net',
        'path': '/',
        'httpOnly': True,
        'secure': True
    })
    driver.get("https://www.acmicpc.net/")


def get_today_workbook_id(driver) -> int:
    from selenium.webdriver.common.by import By

    GROUP_URL = "https://www.acmicpc.net/group/workbook/23567"
    driver.get(GROUP_URL)
    print("현재 페이지:", driver.title)
    print("HTML 일부:", driver.page_source[:1000])
    try:
        # 테이블 로딩까지 최대 10초 기다림
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr"))
        )

        row = driver.find_element(By.CSS_SELECTOR, "table tbody tr")
        link = row.find_element(By.CSS_SELECTOR, "td:nth-child(3) a")
        href = link.get_attribute("href")
        return int(href.split("/")[-1])

    except Exception as e:
        # 🔍 문제 파악을 위해 HTML 저장
        with open("debug_group_page.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        raise RuntimeError("오늘의 워크북을 찾을 수 없습니다.") from e

# ✅ 워크북에서 문제 ID 리스트 추출
def get_problem_ids_from_workbook(driver, group_id: int, workbook_id: int) -> list[int]:
    url = f"https://www.acmicpc.net/group/workbook/view/{group_id}/{workbook_id}"
    driver.get(url)
    rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
    return [int(r.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text) for r in rows]


# ✅ 개별 문제 크롤링
def crawl_boj_problem_with_selenium(driver, problem_id: int) -> dict:
    url = f"https://www.acmicpc.net/problem/{problem_id}"
    print(f"🔍 문제 {problem_id} 크롤링 시작: {url}")
    try:
        driver.get(url)
        time.sleep(random.uniform(1.5, 3.0))

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        def safe_select(selector):
            tag = soup.select_one(selector)
            return tag.text.strip() if tag else ""

        title = safe_select("#problem_title")
        description = safe_select("#problem_description")
        input_desc = safe_select("#problem_input")
        output_desc = safe_select("#problem_output")
        ex_inputs = [pre.text.strip() for pre in soup.select('pre[id^="sample-input-"]')]
        ex_outputs = [pre.text.strip() for pre in soup.select('pre[id^="sample-output-"]')]

        return {
            "problem_number": problem_id,
            "title": title,
            "description": description,
            "input": input_desc,
            "output": output_desc,
            "input_example": ex_inputs,
            "output_example": ex_outputs,
        }

    except Exception as e:
        print(f"[오류] 문제 {problem_id} 처리 실패: {e}")
        return {
            "problem_number": problem_id,
            "title": "",
            "description": "",
            "input": "",
            "output": "",
            "input_example": [],
            "output_example": [],
        }
