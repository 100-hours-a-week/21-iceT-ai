import os, platform, logging
from google.cloud import storage
from langchain_community.vectorstores import FAISS
from src.core.embedding_model import get_embedder
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Google Cloud Storage 설정
GCS_BUCKET = os.getenv("GCS_BUCKET")
GCS_PREFIX = os.getenv("GCS_PREFIX")
LOCAL_INDEX_DIR = os.getenv("LOCAL_INDEX_DIR")

# GCS에서 FAISS 인덱스 파일들 다운로드
def download_faiss_from_gcs():
    # 필요할 때만 GCS에서 인덱스 다운로드
    if os.path.exists(os.path.join(LOCAL_INDEX_DIR, "index.faiss")):
        logger.info("FAISS 인덱스 로컬 캐시 사용")
        return

    logger.info("GCS에서 FAISS 인덱스 다운로드 시작")
    client = storage.Client()
    bucket = client.bucket(GCS_BUCKET)
    blobs = bucket.list_blobs(prefix=GCS_PREFIX)

    os.makedirs(LOCAL_INDEX_DIR, exist_ok=True)
    for blob in blobs:
        if blob.name.endswith("/"):  # 디렉토리 무시
            continue
        filepath = os.path.join(LOCAL_INDEX_DIR, os.path.basename(blob.name))
        blob.download_to_filename(filepath)

    logger.info("GCS에서 FAISS 인덱스 다운로드 완료")

# FAISS 벡터스토어 로딩 (GCS에서 받아온 인덱스 기반)
def load_vectorstore():
    embeddings = get_embedder()

    # ✅ 운영체제에 따라 분기
    if platform.system() == "Windows":
        print("🔍 [RAG] Windows 환경 → 로컬 FAISS 인덱스 로딩")
        return FAISS.load_local(
            "vector/faiss_index",
            embeddings,
            allow_dangerous_deserialization=True
        )

    else:
        print("☁️ [RAG] Linux 환경 → GCP에서 FAISS 인덱스 다운로드")
        download_faiss_from_gcs()
        return FAISS.load_local(
            os.getenv("LOCAL_INDEX_DIR", "vector/faiss_index"),
            embeddings,
            allow_dangerous_deserialization=True
        )
