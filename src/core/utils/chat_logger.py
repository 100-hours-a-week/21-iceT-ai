import csv
import os
from datetime import datetime

BASE_PATH = "DB"  # 저장 경로

def get_next_turn(session_id: str, file: str) -> int:
    """해당 세션의 다음 턴 번호 계산 (2개 메시지마다 1턴)"""
    filepath = os.path.join(BASE_PATH, file)
    if not os.path.exists(filepath):
        return 1
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        # 해당 세션의 메시지 개수 세기
        msg_count = sum(1 for row in reader if row[0] == session_id)
        return (msg_count // 2) + 1

def append_chat_record(session_id: str, role: str, content: str, timestamp: str = None):
    """chat_record.csv: sessionId, turn, role, content, createdAt"""
    filepath = os.path.join(BASE_PATH, "chat_record.csv")
    os.makedirs(BASE_PATH, exist_ok=True)
    
    timestamp = timestamp or datetime.now().isoformat()
    turn = get_next_turn(session_id, "chat_record.csv")
    with open(filepath, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([session_id, turn, role, content, timestamp])

def append_chat_session(session_id: str, problem_number: int, title: str, start_time: str):
    """chat_session.csv: sessionId, problemNumber, title, createdAt"""
    filepath = os.path.join(BASE_PATH, "chat_session.csv")
    os.makedirs(BASE_PATH, exist_ok=True)

    with open(filepath, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([session_id, problem_number, title, start_time])

def append_chat_summary(session_id: str, summary: str, timestamp: str = None):
    """chat_summary.csv: sessionId, turn, summary, createdAt"""
    filepath = os.path.join(BASE_PATH, "chat_summary.csv")
    os.makedirs(BASE_PATH, exist_ok=True)

    timestamp = timestamp or datetime.now().isoformat()
    turn = get_next_turn(session_id, "chat_summary.csv")
    with open(filepath, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([session_id, turn, summary, timestamp])
