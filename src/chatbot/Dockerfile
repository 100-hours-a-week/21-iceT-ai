# 베이스 이미지
FROM python:3.9-slim

# 루트 작업 디렉토x리 설정
WORKDIR /21-iceT-ai

# requirements.txt 복사 및 의존성 설치
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 전체 복사
COPY . .

# FastAPI 서버 실행 (main.py 직접 실행)
CMD ["python", "-m", "src.chatbot.main"]