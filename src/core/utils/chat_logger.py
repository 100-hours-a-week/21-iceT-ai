import csv
import os
from datetime import datetime

BASE_PATH = "DB"  # 저장 경로

def append_chat_record(session_id: str, role: str, content: str, timestamp: str = None):
    """대화 로그 저장"""
    filepath = os.path.join(BASE_PATH, "chat_record.csv")
    timestamp = timestamp or datetime.now().isoformat()
    with open(filepath, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([session_id, role, content, timestamp])

def append_chat_session(session_id: str, problem_number: int, title: str, start_time: str, mode: str):
    """세션 정보 저장"""
    filepath = os.path.join(BASE_PATH, "chat_session.csv")
    with open(filepath, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([session_id, problem_number, title, start_time, mode])

def append_chat_summary(session_id: str, static_summary: str, summary: str, timestamp: str = None):
    """대화 요약 저장"""
    filepath = os.path.join(BASE_PATH, "chat_summary.csv")
    timestamp = timestamp or datetime.now().isoformat()
    with open(filepath, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([session_id, static_summary, summary, timestamp])
