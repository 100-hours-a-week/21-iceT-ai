import requests
import json

url = "http://localhost:8000/api/ai/v2/feedback/answer"
headers = {
    "Content-Type": "application/json"
}

# 📌 요약: 문제 정보 + 대화 요약 포함
summary = [
    {
        "type": "problem",
        "speaker": "system",
        "intent": "문제 정보 요약",
        "content": "이 문제는 정렬된 수열에서 두 수의 합이 목표값이 되는지를 찾는 문제입니다."
    },
    {
        "type": "chat",
        "speaker": "user",
        "intent": "질문",
        "content": "투포인터가 뭔가요?"
    },
    {
        "type": "chat",
        "speaker": "ai",
        "intent": "설명",
        "content": "투포인터는 정렬된 배열에서 두 인덱스를 움직이며 조건을 만족하는 쌍을 찾는 알고리즘입니다."
    }
]

# 📌 메시지: 새로 사용자가 질문한 것
messages = [
    {"role": "user", "content": "그럼 정렬은 항상 필요한가요?"}
]

data = {
    "sessionId": "test-feedback-answer-001",
    "messages": messages,
    "summary": json.dumps(summary)
}

response = requests.post(url, headers=headers, json=data, stream=True)

# 📌 SSE 스트리밍 응답 읽기
print("status:", response.status_code)
if response.status_code == 200:
    print("response:")
    for line in response.iter_lines(decode_unicode=True):
        if line and line.startswith("data: "):
            print(line.removeprefix("data: "), end="", flush=True)
else:
    print("error response:", response.text)
