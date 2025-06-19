import os
import numpy as np
from langchain.schema import Document
from src.loaders.problem_loader import fetch_all_problems
from src.core.embedding_model import get_embedder
from src.core.vector_store_recommend import load_boj_vectorstore

# (예시) 사용자 히스토리 조회 함수. 실제 구현에 맞게 바꾸세요.
def get_user_history(user_id: str) -> tuple[list[int], list[int]]:
    """
    Return two lists of problem IDs:
      - wrong_ids: 사용자가 틀린 문제 ID 리스트
      - unsolved_ids: 사용자가 아직 못 푼 문제 ID 리스트
    """
    # TODO: DB나 캐시에서 user_id 기준으로 불러오기
    return [1491, 11053], [1699, 2583]

def recommend_for_user(
    user_id: str,
    top_k: int = 50,
    final_n: int = 3
) -> list[Document]:
    """
    1) user_id의 히스토리 문제 임베딩 → 평균 벡터(user_vec) 생성
    2) FAISS에서 top_k 후보 검색
    3) 난이도 ±1, 태그 필터링
    4) solve_rate 오름차순 정렬 후 final_n개 리턴
    """
    # Load resources
    vs      = load_boj_vectorstore()
    embedder = get_embedder()

    # 1) 사용자 히스토리
    wrong_ids, unsolved_ids = get_user_history(user_id)
    history_ids = set(wrong_ids + unsolved_ids)
    # 2) 히스토리 텍스트 및 벡터
    id2text = {
        prob["id"]: f"# {prob['title']}\n\n{prob['body']}"
        for prob in fetch_all_problems()
    }
    history_texts = [id2text[i] for i in history_ids]
    history_embs  = embedder.embed_documents(history_texts)
    user_vec      = np.mean(history_embs, axis=0).tolist()

    # 3) 유사도 검색
    candidates: list[Document] = vs.similarity_search_by_vector(user_vec, k=top_k)

    # 4) 메타 필터링: 난이도 ±1, 태그 교집합, 히스토리 제외
    # (실제론 history_ids 기반 avg_diff, top_tags를 계산하세요)
    avg_diff = round(np.mean([doc.metadata["difficulty"] for doc in candidates]))
    top_tags = {"그래프", "DP"}  # 예시: 사용자 히스토리에서 추출
    filtered = [
        doc for doc in candidates
        if abs(doc.metadata["difficulty"] - avg_diff) <= 1
        and set(doc.metadata["tags"]) & top_tags
        and doc.metadata["problem_id"] not in history_ids
    ]

    # 5) 최종 정렬 & 선택
    filtered.sort(key=lambda d: d.metadata["solve_rate"])
    return filtered[:final_n]

# 사용 예 (FastAPI endpoint 등에서 호출)
if __name__ == "__main__":
    recs = recommend_for_user("user123")
    for doc in recs:
        print(doc.metadata["problem_id"], doc.metadata["difficulty"], doc.metadata["tags"])