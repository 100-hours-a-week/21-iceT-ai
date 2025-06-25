# 실행 파일 (매일 아침 10시에 실행)

# 추천 문제 생성을 위한 메인 함수
import logging
from src.core.logger import setup_logging
from src.recommend.recommend_service_v2 import recommend_for_user, send_recommendations

setup_logging()
logger = logging.getLogger(__name__)

def main():
    logger.info("=== Daily recommendation pipeline 시작 ===")
    try:
        combos = recommend_for_user()
        logger.info(f"추천 조합 생성 완료: {combos}")

        send_recommendations(combos)
        logger.info("추천 결과 전송 성공")

    except Exception as e:
        logger.error("파이프라인 실행 중 오류 발생")
        raise

    logger.info("=== Daily recommendation pipeline 종료 ===")

if __name__ == "__main__":
    main()