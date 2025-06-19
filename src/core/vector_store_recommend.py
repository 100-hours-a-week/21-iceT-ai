# 추천 문제 제공을 위한 백준 문제 벡터스토어 로더

import os, logging
from google.cloud import storage
from langchain_community.vectorstores import FAISS
from src.core.embedding_model import get_embedder

logger = logging.getLogger(__name__)

# GCS 설정
GCS_BUCKET = os.getenv("GCS_BUCKET")
GCS_PREFIX_BAEKJOON = os.getenv("GCS_PREFIX_BAEKJOON")
LOCAL_INDEX_BAEKJOON_DIR = os.getenv("LOCAL_INDEX_BAEKJOON_DIR")


def download_boj_index_from_gcs():
    if os.path.exists(os.path.join(LOCAL_INDEX_BAEKJOON_DIR, "index.faiss")):
        logger.info("Using cached BOJ FAISS index")
        return

    logger.info("Downloading BOJ FAISS index from GCS...")
    client = storage.Client()
    bucket = client.bucket(GCS_BUCKET)
    blobs = bucket.list_blobs(prefix=GCS_PREFIX_BAEKJOON)

    os.makedirs(LOCAL_INDEX_BAEKJOON_DIR, exist_ok=True)
    for blob in blobs:
        if blob.name.endswith("/"):
            continue
        dest_path = os.path.join(LOCAL_INDEX_BAEKJOON_DIR, os.path.basename(blob.name))
        blob.download_to_filename(dest_path)
        logger.info(f"Downloaded {blob.name}")


def load_boj_vectorstore() -> FAISS:
    download_boj_index_from_gcs()
    embedder = get_embedder()
    vectorstore = FAISS.load_local(
        LOCAL_INDEX_BAEKJOON_DIR,
        embeddings=embedder,
        allow_dangerous_deserialization=True
    )
    logger.info("BOJ FAISS index loaded into memory")
    return vectorstore
