# 시간복잡도 : 30,000 (백준 문제 수)
# 회원 수 100명 -> 3,000,000

from typing import List
import requests
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever, EnsembleRetriever
from langchain.retrievers import MaximalMarginalRelevanceRetriever, RerankRetriever
from sentence_transformers import CrossEncoder
from src.core.embedding_model import get_embedder
from src.recommend.problem_loader import fetch_all_problems
from src.config import GETPROBLEM_BACKEND_URL, RECOMMEND_BACKEND_URL, BACKEND_TIMEOUT

# 모든 문제 데이터와 매핑 한 번만 로드
_all_probs = list(fetch_all_problems())
_id2meta = {p['id']: p for p in _all_probs}
_id2text = {p['id']: f"# {p['title']}\n\n{p['description']}" for p in _all_probs}

# 티어, 태그 조합별 문제 ID 집합 미리 계산
_problems_by_tier_tag: dict[tuple[int, str], set[int]] = {}
for p in _all_probs:
    for tag in p['tags']:
        _problems_by_tier_tag.setdefault((p['tier'], tag), set()).add(p['id'])

# 전날 출제된 문제 2개 조회
def get_user_history() -> List[int]:
    resp = requests.get(GETPROBLEM_BACKEND_URL, timeout=BACKEND_TIMEOUT)
    resp.raise_for_status()
    return resp.json().get('yesterdayIds', [])[:2]

# 추천 로직: 전날 문제 각각에 대해 tier±1 후보 1개씩 4가지 조합 생성
# (각 candidate set 당 FAISS 인덱스 + BM25/Ensemble/MMR/Rerank)
def recommend_for_user() -> List[List[int]]:
    history = get_user_history()
    embedder = get_embedder()
    results: dict[int, dict[str, int | None]] = {}

    # 하이브리드 retriever 하이퍼파라미터
    bm25_k = 5
    dense_k = 10
    score_threshold = 0.7
    mmr_k = 5
    mmr_lambda = 0.6
    rerank_k = 1
    cross_model = 'cross-encoder/ms-marco-MiniLM-L-6-v2'

    for pid in history:
        meta = _id2meta[pid]
        tier = meta['tier']
        tags = meta['tags']
        dir_map: dict[str, int | None] = {}

        for direction, tgt in (('hi', tier+1), ('lo', max(1, tier-1))):
            cand_ids: set[int] = set()
            for tag in tags:
                cand_ids |= _problems_by_tier_tag.get((tgt, tag), set())

            docs = [Document(page_content=_id2text[i], metadata=_id2meta[i]) for i in cand_ids]
            if not docs:
                dir_map[direction] = None
                continue

            # BM25 리트리버
            bm25 = BM25Retriever.from_documents(docs)
            bm25.k = bm25_k

            # Dense 리트리버
            dense = FAISS.from_documents(docs, embedder).as_retriever(
                search_type='similarity_score_threshold',
                search_kwargs={'k': dense_k, 'score_threshold': score_threshold}
            )

            # Sparse+Dense 앙상블
            ensemble = EnsembleRetriever(
                retrievers=[bm25, dense],
                weights=[0.3, 0.7]
            )

            # MMR 다양성 강화
            mmr = MaximalMarginalRelevanceRetriever(
                retriever=ensemble,
                k=mmr_k,
                lambda_mult=mmr_lambda
            )

            # Cross-Encoder 재랭킹
            cross = CrossEncoder(cross_model)
            reranker = RerankRetriever.from_retriever(
                retriever=mmr,
                cross_encoder=cross,
                k=rerank_k
            )

            # 최종 1개 추천
            top_docs = reranker.invoke(_id2text[pid], top_k=1)
            dir_map[direction] = top_docs[0].metadata['id'] if top_docs else None

        results[pid] = dir_map

    p1, p2 = history
    c1, c2 = results[p1], results[p2]
    combos = [
        [c1['hi'], c2['hi']],
        [c1['lo'], c2['hi']],
        [c1['hi'], c2['lo']],
        [c1['lo'], c2['lo']],
    ]
    return combos

# 추천 결과 백엔드로 전송
def send_recommendations(combos: List[List[int]]) -> None:
    payload = {'recommendations': combos}
    resp = requests.post(RECOMMEND_BACKEND_URL, json=payload, timeout=BACKEND_TIMEOUT)
    resp.raise_for_status()
    print('백엔드 전송 성공:', resp.json())