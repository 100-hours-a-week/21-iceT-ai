# src/adapters/llm_key_manager.py

import time
from threading import Lock
from src.config import settings

class APIKeyManager:
    def __init__(self, keys: list[str], rpm_limit=100, tpm_limit=100000):
        self.keys = keys
        self.rpm_limit = rpm_limit
        self.tpm_limit = tpm_limit
        self.lock = Lock()
        self.usage = {
            key: {
                "count": 0,       # 요청 수 (RPM)
                "tokens": 0,      # 토큰 수 (TPM)
                "last_reset": time.time()
            }
            for key in keys
        }

    def select_least_busy_key(self) -> str:
        now = time.time()
        with self.lock:
            for key, state in self.usage.items():
                if now - state["last_reset"] > 60:
                    state["count"] = 0
                    state["tokens"] = 0
                    state["last_reset"] = now

            # 요청 수와 토큰 수를 기준으로 가장 덜 바쁜 키 선택
            sorted_keys = sorted(self.keys, key=lambda k: (self.usage[k]["count"], self.usage[k]["tokens"]))
            return sorted_keys[0]

    def record_usage(self, key: str, tokens: int):
        with self.lock:
            if key not in self.usage:
                return
            self.usage[key]["count"] += 1
            self.usage[key]["tokens"] += tokens


# ✅ 클래스 정의 이후에 객체 생성
api_key_manager = APIKeyManager(
    keys=settings.upstage_key_list,
    rpm_limit=100,
    tpm_limit=100_000
)
