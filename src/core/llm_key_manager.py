# src/core/llm_key_manager.py
import itertools
import os

class APIKeyManager:
    def __init__(self, keys_env: str):
        keys = [k.strip() for k in keys_env.split(",") if k.strip()]
        if not keys:
            raise ValueError("API 키가 존재하지 않습니다.")
        self._cycle = itertools.cycle(keys)

    def next_key(self):
        return next(self._cycle)
