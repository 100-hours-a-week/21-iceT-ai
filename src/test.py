import os
from dotenv import load_dotenv
from openai import OpenAI

# .env 로드
load_dotenv()

# 키 로드 및 정리
raw_keys = os.getenv("SOLAR_API_KEYS", "")
solar_keys = [k.strip() for k in raw_keys.split(",") if k.strip()]

# 인덱스 선택
key_index = 1  # 0~9 사이에서 지정

# 사용 키 확인 (일부 마스킹)
selected_key = solar_keys[key_index]
print(f"[INFO] 테스트 중인 키 (index {key_index}): {selected_key[:8]}...")

# 클라이언트 초기화
client = OpenAI(
    api_key=selected_key,
    base_url="https://api.upstage.ai/v1"
)

# LLM 호출
response = client.chat.completions.create(
    model="solar-pro",
    messages=[{"role": "user", "content": "간단한 수학 문제 하나만 내줘."}],
    max_tokens=100,
    temperature=0.5
)

# 응답 출력
print("=== 응답 ===")
print(response.choices[0].message.content)
