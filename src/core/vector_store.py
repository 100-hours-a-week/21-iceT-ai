# src/core/vector_store.py
import os, logging
from google.cloud import storage
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

def get_embedder():
    return HuggingFaceEmbeddings(
        model_name="intfloat/multilingual-e5-base",
        encode_kwargs={"normalize_embeddings": True}
    )

USE_GCS = os.getenv("USE_GCS_FOR_FAISS", "false").lower() == "true"
GCS_BUCKET = os.getenv("GCS_BUCKET")
GCS_PREFIX = os.getenv("GCS_PREFIX")
LOCAL_INDEX_DIR = os.getenv("LOCAL_INDEX_DIR")

def download_faiss_from_gcs():
    if os.path.exists(os.path.join(LOCAL_INDEX_DIR, "index.faiss")):
        logger.info("✅ FAISS 인덱스 로컬 캐시 사용")
        return

    logger.info("☁️ GCS에서 FAISS 인덱스 다운로드 시작")
    client = storage.Client()
    bucket = client.bucket(GCS_BUCKET)
    blobs = bucket.list_blobs(prefix=GCS_PREFIX)

    os.makedirs(LOCAL_INDEX_DIR, exist_ok=True)
    for blob in blobs:
        if blob.name.endswith("/"):
            continue
        filepath = os.path.join(LOCAL_INDEX_DIR, os.path.basename(blob.name))
        blob.download_to_filename(filepath)

    logger.info("✅ GCS에서 FAISS 인덱스 다운로드 완료")

def load_vectorstore():
    try:
        if not LOCAL_INDEX_DIR:
            raise ValueError("LOCAL_INDEX_DIR 환경변수가 설정되지 않았습니다.")

        if USE_GCS:
            download_faiss_from_gcs()
        elif not os.path.exists(os.path.join(LOCAL_INDEX_DIR, "index.faiss")):
            raise FileNotFoundError("로컬 FAISS 인덱스가 존재하지 않습니다.")

        embedder = get_embedder()
        return FAISS.load_local(
            LOCAL_INDEX_DIR,
            embeddings=embedder,
            allow_dangerous_deserialization=True
        )

    except Exception as e:
        logger.error(f"❌ 벡터스토어 로딩 오류: {e}")
        raise e
