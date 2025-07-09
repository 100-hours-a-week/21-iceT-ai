# 시간복잡도 : 30,000 (백준 문제 수)
# 회원 수 100명 -> 3,000,000

from typing import List
import requests
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from adapters.embedding_model import get_embedder
from src.recommend.problem_loader import fetch_all_problems
from src.config import GETPROBLEM_BACKEND_URL, RECOMMEND_BACKEND_URL, BACKEND_TIMEOUT

# 모든 문제 데이터와 매핑 한 번만 로드
_all_probs = list(fetch_all_problems())
_id2meta = {p["id"]: p for p in _all_probs}
_id2text = {p["id"]: f"# {p['title']}\n\n{p['description']}" for p in _all_probs}

# 티어, 태그 조합별 문제 ID 집합 미리 계산
_problems_by_tier_tag = {}
for p in _all_probs:
    for tag in p["tags"]:
        _problems_by_tier_tag.setdefault((p["tier"], tag), set()).add(p["id"])

# 전날 출제된 문제 2개 조회
def get_user_history() -> List[int]:
    resp = requests.get(GETPROBLEM_BACKEND_URL, timeout=BACKEND_TIMEOUT)
    resp.raise_for_status()
    data = resp.json()
    return data["yesterdayIds"][:2]

# 추천 로직: 전날 문제 각각에 대해 tier±1 후보 1개씩 4가지 조합 생성
def recommend_for_user() -> list[list[int]]:
    problems = get_user_history()
    embedder = get_embedder()

    hi_lo = {}
    for pid in problems:
        meta = _id2meta[pid]
        tier = meta["tier"]
        tags = meta["tags"]

        candidates = {}
        for direction, tgt in (("hi", tier + 1), ("lo", max(1, tier - 1))):
            cand_ids = set()
            for tag in tags:
                cand_ids |= _problems_by_tier_tag.get((tgt, tag), set())

            docs = [Document(page_content=_id2text[i], metadata=_id2meta[i]) for i in cand_ids]
            retriever = FAISS.from_documents(
                documents=docs,
                embedding=embedder,
                index_name=f"tmp_{pid}_{direction}",
                metadatas=[d.metadata for d in docs],
            ).as_retriever()

            query = _id2text[pid]
            top_doc = retriever.invoke(query, top_k=1)[0]
            candidates[direction] = top_doc.metadata["id"]

        hi_lo[pid] = candidates

    p1, p2 = problems
    c1, c2 = hi_lo[p1], hi_lo[p2]
    combos = [
        [c1["hi"], c2["hi"]],
        [c1["lo"], c2["hi"]],
        [c1["hi"], c2["lo"]],
        [c1["lo"], c2["lo"]],
    ]

    return combos

# 추천 결과 백엔드로 전송
def send_recommendations(combos: List[List[int]]) -> None:
    payload = {"recommendations": combos}
    resp = requests.post(RECOMMEND_BACKEND_URL, json=payload, timeout=BACKEND_TIMEOUT)
    resp.raise_for_status()
    print("백엔드 전송 성공:", resp.json()) 