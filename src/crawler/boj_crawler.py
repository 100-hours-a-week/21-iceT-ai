import os
import time
import random
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

load_dotenv()

GROUP_URL = "https://www.acmicpc.net/group/workbook/23567"

# ✅ 셀레니움 드라이버 생성
def create_driver():
    options = Options()
    options.binary_location = "/home/ubuntu/chrome/chrome-linux64/chrome"
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    )

    service = Service("/home/ubuntu/chrome/chromedriver-linux64/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    # 봇 탐지 우회
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
    })

    return driver


# ✅ 로그인 쿠키 추가
def login_with_cookies(driver):
    driver.get("https://www.acmicpc.net/")
    driver.add_cookie({
        'name': 'OnlineJudge',
        'value': os.getenv("BOJ_COOKIE_ONLINEJUDGE"),
        'domain': '.acmicpc.net',
        'path': '/',
        'httpOnly': True,
        'secure': True
    })
    driver.add_cookie({
        'name': 'bojautologin',
        'value': os.getenv("BOJ_COOKIE_AUTOLOGIN"),
        'domain': '.acmicpc.net',
        'path': '/',
        'httpOnly': True,
        'secure': True
    })
    driver.get("https://www.acmicpc.net/")


# ✅ 오늘의 워크북 ID 가져오기
def get_today_workbook_id(driver) -> int:
    driver.get(GROUP_URL)
    try:
        row = driver.find_element(By.CSS_SELECTOR, "table tbody tr")
        link = row.find_element(By.CSS_SELECTOR, "td:nth-child(3) a")
        href = link.get_attribute("href")
        return int(href.split("/")[-1])
    except NoSuchElementException:
        raise RuntimeError("오늘의 워크북을 찾을 수 없습니다.")


# ✅ 워크북에서 문제 ID 리스트 추출
def get_problem_ids_from_workbook(driver, group_id: int, workbook_id: int) -> list[int]:
    url = f"https://www.acmicpc.net/group/workbook/view/{group_id}/{workbook_id}"
    driver.get(url)
    rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
    return [int(r.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text) for r in rows]


# ✅ 개별 문제 크롤링
def crawl_boj_problem_with_selenium(driver, problem_id: int) -> dict:
    url = f"https://www.acmicpc.net/problem/{problem_id}"
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
