# 기본 베이스 이미지를 python:3.9-slim으로 설정
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /crawler

# 필수 패키지 설치 및 타임존 설정
RUN apt-get update && apt-get install -y \
    unzip \
    curl \
    wget \
    gnupg \
    tzdata \  
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    libxrender1 \
    libx11-xcb1 \
    libxcb1 \
    libxcb-glx0 \
    libasound2 \
    libgbm1 \
    libatk1.0-0 \
    libxcomposite1 \
    libxrandr2 \
    libxi6 \
    libgtk-3-0 \
    libcairo2 \
    libpango-1.0-0 \
    && ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime \
    && echo "Asia/Seoul" > /etc/timezone \  
    && rm -rf /var/lib/apt/lists/*  

# Chrome 버전 설정
ENV CHROME_VERSION="133.0.6943.98"

# 최신 Chrome 설치
RUN mkdir -p /crawler/chrome && \
    wget -q "https://storage.googleapis.com/chrome-for-testing-public/$CHROME_VERSION/linux64/chrome-linux64.zip" -O /tmp/chrome.zip && \
    unzip /tmp/chrome.zip -d /tmp/ && \
    mv /tmp/chrome-linux64/* /crawler/chrome/ && \
    rm -rf /tmp/chrome.zip /tmp/chrome-linux64 && \
    chmod +x /crawler/chrome/chrome && \
    ln -s /crawler/chrome/chrome /usr/bin/google-chrome

# ChromeDriver 설치
RUN wget -q "https://storage.googleapis.com/chrome-for-testing-public/$CHROME_VERSION/linux64/chromedriver-linux64.zip" -O /tmp/chromedriver.zip && \
    unzip /tmp/chromedriver.zip -d /tmp/ && \
    mv /tmp/chromedriver-linux64/chromedriver /crawler/chrome/chromedriver && \
    rm -rf /tmp/chromedriver.zip /tmp/chromedriver-linux64 && \
    chmod +x /crawler/chrome/chromedriver

# 사용자 생성
RUN useradd -ms /bin/bash user

# 권한 변경 (기존 사용자에게 전체 접근 권한 부여)
RUN chown -R root:root /crawler && chmod -R 755 /crawler

# 로그 디렉토리 생성 및 권한 설정
RUN mkdir -p /crawler/logs && chown -R root:root /crawler/logs && chmod -R 755 /crawler/logs

# 사용자 변경
USER root

# 최신 pip 버전으로 업데이트
RUN pip install --upgrade pip

# requirements.txt만 먼저 복사
COPY requirements.txt /crawler/requirements.txt

# pip install
RUN pip install -r /crawler/requirements.txt

ENV PYTHONPATH="/crawler"

# 나머지 소스 복사
COPY . /crawler

# cron 및 nano 설치
RUN apt-get update && apt-get install -y cron nano

# 크론탭 파일 추가
COPY crontab /etc/cron.d/daily-crawler-cron

# 크론탭 권한 설정
RUN chmod 0644 /etc/cron.d/daily-crawler-cron

# 크론 서비스 실행을 위한 엔트리포인트 스크립트 추가
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

RUN mkdir -p /crawler/tmp_profile && chmod -R 777 /crawler/tmp_profile

# 엔트리포인트 지정
ENTRYPOINT ["/docker-entrypoint.sh"]
