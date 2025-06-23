import requests

url = "http://localhost:8000/api/ai/v2/feedback/start"
headers = {
    "Content-Type": "application/json",
    "x-api-key": "YOUR_REAL_API_KEY"
}
data = {
    "sessionId": "test-session-1",
    "problemNumber": 1000,
    "title": "A+B",
    "description": "두 정수를 입력받아 합을 출력",
    "inputRule": "두 정수 A와 B가 주어진다",
    "outputRule": "A+B를 출력한다",
    "inputExample": "1 2",
    "outputExample": "3",
    "codeLanguage": "python",
    "code": "a, b = map(int, input().split()); print(a + b)"
}

response = requests.post(url, headers=headers, json=data, stream=True)
for line in response.iter_lines(decode_unicode=True):
    if line and line.startswith("data: "):
        print(line.removeprefix("data: "), end="", flush=True)
