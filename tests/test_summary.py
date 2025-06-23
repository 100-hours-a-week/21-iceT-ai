import requests

url = "http://localhost:8000/api/ai/v2/summary"
headers = {
    "Content-Type": "application/json",
}

# 메시지 12개 생성 (10개 초과)
messages = [
    {"role": "user", "content": "이 문제는 정렬된 수열에서 두 수의 합이 특정 값이 되는 경우를 찾는 문제예요."},
    {"role": "assistant", "content": "그렇다면 투포인터 알고리즘이 적합할 것 같습니다."},

    {"role": "user", "content": "투포인터가 뭔가요?"},
    {"role": "assistant", "content": "정렬된 배열에서 두 인덱스를 양쪽에서 출발시켜 조건을 만족하는 쌍을 찾는 방식입니다."},

    {"role": "user", "content": "이 문제에서 정렬은 이미 되어 있다고 가정해도 되나요?"},
    {"role": "assistant", "content": "문제 설명에 정렬되어 있다고 명시되어 있다면, 바로 투포인터를 적용해도 됩니다."},

    {"role": "user", "content": "시간복잡도는 어떻게 돼요?"},
    {"role": "assistant", "content": "정렬된 상태라면 O(n)에 두 포인터만 움직이므로 전체 시간복잡도는 O(n)입니다."},

    {"role": "user", "content": "구현이 잘 안 되는데 코드 좀 보여주세요."},
    {"role": "assistant", "content": "다음은 Python으로 구현한 예시입니다:\n\n```python\ndef two_sum(arr, target):\n    left, right = 0, len(arr) - 1\n    while left < right:\n        s = arr[left] + arr[right]\n        if s == target:\n            return left, right\n        elif s < target:\n            left += 1\n        else:\n            right -= 1\n    return -1, -1\n```"},

    {"role": "user", "content": "이게 투포인터인가요?"},
    {"role": "assistant", "content": "네, `left`와 `right` 두 포인터를 이동시키면서 합을 비교하는 방식이 투포인터입니다."},

    {"role": "user", "content": "혹시 중복된 수가 있을 때도 이 코드가 동작하나요?"},
    {"role": "assistant", "content": "네, 중복 값이 있어도 합이 조건만 만족하면 해당 인덱스를 반환합니다."},

    {"role": "user", "content": "그럼 정렬되지 않은 경우에는 어떻게 하죠?"},
    {"role": "assistant", "content": "그 경우 먼저 배열을 정렬한 후 투포인터를 적용해야 하므로 전체 시간복잡도는 O(n log n)입니다."},

    {"role": "user", "content": "정렬하면 인덱스가 바뀌지 않나요?"},
    {"role": "assistant", "content": "맞습니다. 그래서 정렬 전에 원래 인덱스를 저장해두거나, 딕셔너리 기반 접근이 필요할 수 있습니다."},

    {"role": "user", "content": "이 문제를 해시맵으로도 풀 수 있나요?"},
    {"role": "assistant", "content": "네, 해시맵을 사용하면 O(n) 시간에 정렬 없이도 풀 수 있습니다. 다만 인덱스가 필요합니다."},

    {"role": "user", "content": "해시맵 풀이도 코드로 보여주세요."},
    {"role": "assistant", "content": "다음은 해시맵을 사용한 예시입니다:\n\n```python\ndef two_sum_hash(arr, target):\n    seen = {}\n    for i, num in enumerate(arr):\n        if target - num in seen:\n            return seen[target - num], i\n        seen[num] = i\n    return -1, -1\n```"},

    {"role": "user", "content": "감사합니다!"},
    {"role": "assistant", "content": "언제든 질문 주세요 😊"},

    {"role": "user", "content": "추가로 시간복잡도 비교 정리해 주세요."},
    {"role": "assistant", "content": "- 정렬 + 투포인터: O(n log n)\n- 정렬된 배열 + 투포인터: O(n)\n- 해시맵: O(n), 정렬 불필요"},

    {"role": "user", "content": "두 방법 중 뭐가 더 나을까요?"},
    {"role": "assistant", "content": "정렬된 배열이면 투포인터, 아니면 해시맵이 구현 간편하고 빠릅니다."},

    {"role": "user", "content": "문제에 여러 쌍이 있을 수도 있는데요?"},
    {"role": "assistant", "content": "그 경우에는 인덱스를 저장해서 모든 조합을 리스트에 넣도록 코드를 수정해야 합니다."},

    {"role": "user", "content": "그것도 해주세요."},
    {"role": "assistant", "content": "다음은 모든 쌍을 찾는 코드입니다:\n\n```python\ndef all_two_sum(arr, target):\n    res = []\n    seen = {}\n    for i, num in enumerate(arr):\n        complement = target - num\n        if complement in seen:\n            res.append((seen[complement], i))\n        seen[num] = i\n    return res\n```"},

    {"role": "user", "content": "아하 정리 감사합니다!"}
]

data = {
    "sessionId": "test-summary-10over",
    "messages": messages,
    "maxSentences": 5,
    "mode": "feedback"
}

response = requests.post(url, headers=headers, json=data)
print("status:", response.status_code)
print("response:", response.json())