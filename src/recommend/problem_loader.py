# 백준 문제 데이터 로더

import csv, logging
from pathlib import Path

logger = logging.getLogger(__name__)

CSV_PATH = Path(__file__).resolve().parents[1] / "data" / "boj.csv"

# CSV에서 모든 문제 데이터 조회
def fetch_all_problems():
    if not CSV_PATH.is_file():
        logger.error(f"CSV 파일이 없습니다: {CSV_PATH}")
        return

    with CSV_PATH.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                yield {
                    "id":          int(row["id"]),
                    "title":       row["title"],
                    "description": row["description"],
                    "tier":        int(float(row["tier"])),  # 1.0 → 1
                    "tags":        [t.strip() for t in row["tags"].split(",") if t.strip()]
                }
            except (KeyError, ValueError) as e:
                continue
