import requests
import json

API_URL = "http://localhost:8000/api/ai/v2/feedback/start/"

payload = {
    "sessionId": "test-session-1234",  # ✅ 추가됨
    "problemNumber": 1000,
    "title": "A+B",
    "description": "두 정수 A와 B를 입력받은 다음, A+B를 출력하는 문제",
    "inputRule": "두 정수 A와 B가 주어진다.",
    "outputRule": "A+B를 출력한다.",
    "inputExample": "1 2",  # ✅ 오타 수정 (intput → input)
    "outputExample": "3",
    "codeLanguage": "python",
    "code": "a, b = map(int, input().split())\nprint(a + b)"
}

try:
    response = requests.post(API_URL, json=payload)
    response.raise_for_status()  # 상태코드가 4xx/5xx면 예외 발생
    print("✅ 요청 성공")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
except requests.exceptions.HTTPError as http_err:
    print(f"❌ HTTP 에러: {http_err}")
    print("응답 내용:", response.text)
except Exception as err:
    print(f"❌ 기타 에러: {err}")
