# 테스트 코드
# 실행 방법 : python -m pytest -s tests/test_recommend_pipeline.py

import pytest
from src.recommend.recommend_service_v2 import recommend_for_user


@pytest.mark.asyncio
async def test_recommend_for_user_pipeline():
    test_history = [14291, 28586] #호텔, 바이러스
    combos = recommend_for_user(history=test_history)
    print("추천 결과:", combos)