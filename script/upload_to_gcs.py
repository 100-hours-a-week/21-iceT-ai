from google.cloud import storage
import os, logging, dotenv

# 로깅
logger = logging.getLogger(__name__)

# 환경변수 설정
dotenv.load_dotenv()

# Google Cloud Storage 설정
bucket_name = os.getenv("GCS_BUCKET")
tmp_dir = os.getenv("VECTOR_STORE_PATH")
source_dir = f"../{tmp_dir}"
destination_prefix = os.getenv("GCS_PREFIX")

# GCS 클라이언트 생성
# TODO: GCP 서비스 키, 환경변수 설정 필요
client = storage.Client()
bucket = client.bucket(bucket_name)

# 업로드
for filename in os.listdir(source_dir):
    local_path = os.path.join(source_dir, filename)
    blob = bucket.blob(f"{destination_prefix}/{filename}")
    blob.upload_from_filename(local_path)
    logger.info(f" 업로드 완료: {blob.name}")