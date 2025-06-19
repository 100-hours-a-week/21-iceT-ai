# GCS에 백준 벡터스토어 업로드
# 서버 실행 전 1회 실행 필요

import os, logging
from google.cloud import storage
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

bucket_name = os.getenv("GCS_BUCKET")
prefix = os.getenv("GCS_PREFIX_BAEKJOON")  # e.g. "vector/faiss_index_baekjoon"
local_dir = os.getenv("VECTOR_STORE_BAEKJOON_PATH")

client = storage.Client()
bucket = client.bucket(bucket_name)

for filename in os.listdir(local_dir):
    local_path = os.path.join(local_dir, filename)
    blob_path = f"{prefix}/{filename}"
    bucket.blob(blob_path).upload_from_filename(local_path)
    logger.info(f"Uploaded {blob_path}")

print("✅ BOJ index uploaded to GCS")