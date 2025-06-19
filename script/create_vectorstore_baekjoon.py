# 추천 문제 제공을 위한 백준 벡터스토어 생성
# 서버 실행 전 1회 실행 필요

import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from src.core.embedding_model import get_embedder
from src.loaders.problem_loader import load_boj_problems

load_dotenv()

docs = load_boj_problems()

embedder = get_embedder()
vectorstore = FAISS.from_documents(
    documents=docs,
    embedding=embedder,
    index_name="baekjoon_problems",
    metadatas=[doc.metadata for doc in docs],
)

out_path = os.getenv("VECTOR_STORE_BAEKJOON_PATH", "vector/faiss_index_baekjoon")
os.makedirs(out_path, exist_ok=True)
vectorstore.save_local(out_path)
print(f"Vectorstore saved to {out_path}")