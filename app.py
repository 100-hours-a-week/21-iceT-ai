import streamlit as st
import httpx
import uuid
import pandas as pd
from datetime import datetime
from pathlib import Path

BASE_URL = "http://localhost:8000/api/ai/v2"

# CSV 경로
session_csv = Path("chat_session.csv")
record_csv = Path("chat_record.csv")
summary_csv = Path("chat_summary.csv")

def append_csv(path, data):
    df = pd.DataFrame([data])
    if path.exists():
        df.to_csv(path, mode='a', index=False, header=False)
    else:
        df.to_csv(path, index=False)

# UI 구성
st.set_page_config(page_title="AI 챗봇", layout="centered")
st.title("💬 Koco AI 챗봇 (면접 & 피드백 모드)")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.turn = 1
    st.session_state.messages = []
    st.session_state.started = False
    st.session_state.mode = "feedback"
    st.session_state.start_payload = {}

# 모드 선택
mode = st.radio("모드를 선택하세요", ["feedback", "interview"])
st.session_state.mode = mode

# START 입력
# 문제 입력 폼 개선
with st.form("start_form"):
    st.subheader("📌 문제 정보 입력")

    col1, col2 = st.columns([1, 3])
    with col1:
        problem_number = st.number_input("문제 번호", value=1157, step=1)
    with col2:
        title = st.text_input("문제 제목", value="단어 공부")

    description = st.text_area("문제 설명", value=(
        "알파벳 대소문자로 이루어진 단어가 주어졌을 때, "
        "가장 많이 사용된 알파벳을 출력하는 프로그램을 작성하시오. "
        "단, 대문자와 소문자를 구분하지 않는다. "
        "가장 많이 사용된 알파벳이 여러 개 존재하는 경우에는 ?를 출력한다."
    ), height=130)

    input_rule = st.text_area("입력 조건", value=(
        "첫째 줄에 알파벳 대소문자로 이루어진 단어가 주어진다. "
        "주어지는 단어는 1,000,000자를 넘지 않는다."
    ), height=80)

    output_rule = st.text_area("출력 조건", value=(
        "첫째 줄에 이 단어에서 가장 많이 사용된 알파벳을 출력한다. "
        "단, 가장 많이 사용된 알파벳이 여러 개 존재하는 경우에는 ?를 출력한다."
    ), height=80)

    input_example = st.text_input("입력 예시", value="Mississipi")
    output_example = st.text_input("출력 예시", value="?")

    code = st.text_area("사용자 제출 코드", value=(
        'word = input().upper()\n'
        'counter = {}\n'
        'for ch in word:\n'
        '    if ch in counter:\n'
        '        counter[ch] += 1\n'
        '    else:\n'
        '        counter[ch] = 1\n\n'
        'max_count = max(counter.values())\n'
        'result = [k for k, v in counter.items() if v == max_count]\n\n'
        'if len(result) > 1:\n'
        '    print("?")\n'
        'else:\n'
        '    print(result[0])'
    ), height=220)

    language = st.selectbox("프로그래밍 언어", ["python", "cpp", "java"], index=0)

    submitted = st.form_submit_button("🚀 START 요청 보내기")


if submitted and not st.session_state.started:
    st.session_state.start_payload = {
        "sessionId": st.session_state.session_id,
        "problemNumber": int(problem_number),
        "title": title,
        "description": description,
        "inputRule": input_rule,
        "outputRule": output_rule,
        "inputExample": input_example,
        "outputExample": output_example,
        "codeLanguage": language,
        "code": code
    }

    endpoint = "/feedback/start" if st.session_state.mode == "feedback" else "/interview/start"
    res = httpx.post(f"{BASE_URL}{endpoint}", json=st.session_state.start_payload, timeout=60.0)
    response = res.json()

    # 메시지 초기화
    st.session_state.messages = [
        { "role": "user", "content": f"{description}\n코드:\n{code}" },
        { "role": "assistant", "content": response.get("improvedCode") or response.get("question") }
    ]

    append_csv(session_csv, {
        "sessionId": st.session_state.session_id,
        "problemNumber": 1000,
        "title": title,
        "createdAt": datetime.utcnow().isoformat()
    })

    append_csv(record_csv, {
        "sessionId": st.session_state.session_id,
        "turn": st.session_state.turn,
        "role": "user",
        "content": st.session_state.messages[0]["content"],
        "createdAt": datetime.utcnow().isoformat()
    })
    append_csv(record_csv, {
        "sessionId": st.session_state.session_id,
        "turn": st.session_state.turn,
        "role": "assistant",
        "content": st.session_state.messages[1]["content"],
        "createdAt": datetime.utcnow().isoformat()
    })

    st.session_state.turn += 1
    st.session_state.started = True
    st.success("초기 요청 완료!")

# 채팅 인터페이스
if st.session_state.started:
    user_input = st.chat_input("질문을 입력하세요")
    if user_input:
        st.session_state.messages.append({ "role": "user", "content": user_input })
        append_csv(record_csv, {
            "sessionId": st.session_state.session_id,
            "turn": st.session_state.turn,
            "role": "user",
            "content": user_input,
            "createdAt": datetime.utcnow().isoformat()
        })

        # 피드백/면접 구분
        if st.session_state.mode == "feedback":
            payload = {
                "sessionId": st.session_state.session_id,
                "messages": st.session_state.messages,
                "summary": None
            }
            res = httpx.post(f"{BASE_URL}/feedback/answer", json=payload, timeout=60.0)
            answer = res.json()["answer"]
        else:
            payload = {
                "sessionId": st.session_state.session_id,
                "messages": st.session_state.messages
            }
            res = httpx.post(f"{BASE_URL}/interview/answer", json=payload)
            answer = res.json()["question"]

        st.session_state.messages.append({ "role": "assistant", "content": answer })
        append_csv(record_csv, {
            "sessionId": st.session_state.session_id,
            "turn": st.session_state.turn,
            "role": "assistant",
            "content": answer,
            "createdAt": datetime.utcnow().isoformat()
        })

        # 5턴마다 요약
        if st.session_state.turn % 5 == 0:
            summary_payload = {
                "sessionId": st.session_state.session_id,
                "mode": st.session_state.mode,
                "messages": st.session_state.messages[-10:]  # 최근 5턴
            }
            res = httpx.post(f"{BASE_URL}/summary", json=summary_payload, timeout=60.0)
            summary_response = res.json()
            summary_text = summary_response.get("summary") or summary_response.get("answer")

            append_csv(summary_csv, {
                "sessionId": st.session_state.session_id,
                "turn": st.session_state.turn,
                "summary": summary_text,
                "createdAt": datetime.utcnow().isoformat()
            })

            st.info(f"🧠 요약 생성됨 (TURN {st.session_state.turn})\n\n{summary_text}")

        st.session_state.turn += 1

    # 대화 출력
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
