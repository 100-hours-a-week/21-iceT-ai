# 백준 문제 데이터 로더

import requests, logging
from src.config import BAEKJUN_BACKEND_URL, BACKEND_TIMEOUT

logger = logging.getLogger(__name__)

# 백엔드에서 모든 문제 목록 조회
def fetch_all_problems():
    try:
        resp = requests.get(BAEKJUN_BACKEND_URL, timeout=BACKEND_TIMEOUT)
        resp.raise_for_status()
        problems = resp.json()
    except requests.RequestException as e:
        logger.error(f"GET 요청 실패: {e}")
        return
    
    for p in problems:
        yield {
            "id":          p["id"],
            "title":       p["title"],
            "description": p["description"],
            "tier":        p["tier"],
            "tags":        p["tags"]
        }