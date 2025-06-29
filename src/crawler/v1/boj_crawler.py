from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import random
import os
from dotenv import load_dotenv

load_dotenv()

# Selenium Chrome 드라이버 생성 함수
def create_driver():
    options = Options()
    options.binary_location = "/home/ubuntu/chrome/chrome-linux64/chrome"
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/115.0.0.0 Safari/537.36")

    service = Service("/home/ubuntu/chrome/chromedriver-linux64/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
       "source": """
           Object.defineProperty(navigator, 'webdriver', {
               get: () => undefined
           })
       """
    })
    return driver

# 로그인 쿠키 추가 함수
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


# 백준 문제를 크롤링하는 함수
def crawl_boj_problem_with_selenium(driver, problem_id):
    url = f"https://www.acmicpc.net/problem/{problem_id}"
    try:
        driver.get(url)
        time.sleep(random.uniform(1.5, 3.0))
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        def safe_select(selector):
            tag = soup.select_one(selector)
            return tag.text.strip() if tag else ""

        # 문제 구성 요소 파싱
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
            "output_example": ex_outputs
        }

    except Exception as e:
        print(f"[오류] 문제 {problem_id} 처리 실패: {e}")
        return {
            "problem_number": problem_id,
            "title": "",
            "description": "",
            "input": "",
            "output": "",
            "input_example": "",
            "output_example": ""
        }
    

# 로컬에서 실행 가능한 코드

# def create_driver():
#     options = Options()
#     options.add_argument("--headless=new")
#     options.add_argument("--disable-gpu")
#     options.add_argument("--no-sandbox")
#     options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")

#     service = Service("/Users/junsu/Downloads/chromedriver-mac-arm64/chromedriver")
#     driver = webdriver.Chrome(service=service, options=options)
#     return driver

# def login_with_cookies(driver):
#     driver.get("https://www.acmicpc.net/")
#     driver.add_cookie({
#         'name': 'OnlineJudge',
#         'value': os.getenv("BOJ_COOKIE_ONLINEJUDGE"),
#         'domain': '.acmicpc.net',
#         'path': '/',
#         'httpOnly': True,
#         'secure': True
#     })
#     driver.add_cookie({
#         'name': 'bojautologin',
#         'value': os.getenv("BOJ_COOKIE_AUTOLOGIN"),
#         'domain': '.acmicpc.net',
#         'path': '/',
#         'httpOnly': True,
#         'secure': True
#     })

# USER_AGENTS = [
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
#     "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0",
#     "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1"
# ]