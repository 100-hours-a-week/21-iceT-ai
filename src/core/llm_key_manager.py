import heapq
import time
import threading
import logging

logger = logging.getLogger(__name__)

class APIKeyManager:
    def __init__(self, keys, default_cooldown_sec=60):
        self.lock = threading.Lock()
        self.cooldown = default_cooldown_sec

        self.key_next_available = {key: 0.0 for key in keys}

        self.pq = [(0.0, key) for key in keys]
        heapq.heapify(self.pq)

    def next_key(self):
        with self.lock:
            while True:
                next_avail, key = heapq.heappop(self.pq)

                if self.key_next_available[key] != next_avail:
                    continue
                now = time.time()

                if next_avail > now:
                    time.sleep(next_avail - now)
                    now = time.time()

                next_time = now + self.cooldown
                self.key_next_available[key] = next_time
                heapq.heappush(self.pq, (next_time, key))
                # 마스킹: 앞 4글자 + ... + 뒤 4글자
                if len(key) > 8:
                    masked = f"{key[:4]}...{key[-4:]}"
                else:
                    masked = key
                logger.info(f"[APIKeyManager] 사용 API KEY: {masked}")
                print(f"[APIKeyManager] 사용 API KEY: {masked}")
                return key

    def mark_rate_limited(self, key, retry_after_sec):
        with self.lock:
            now = time.time()
            next_time = now + retry_after_sec
            self.key_next_available[key] = next_time
            heapq.heappush(self.pq, (next_time, key))