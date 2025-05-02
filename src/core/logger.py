import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = os.getenv("LOG_DIR", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

def setup_logging():
    fmt = "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
    logging.basicConfig(
        level=logging.INFO,
        format=fmt,
        handlers=[
            logging.StreamHandler(),  # 콘솔 출력
            RotatingFileHandler(      # 파일 기록
                filename=os.path.join(LOG_DIR, "app.log"),
                maxBytes=10*1024*1024,
                backupCount=5,
                encoding="utf-8",
            )
        ],
    )