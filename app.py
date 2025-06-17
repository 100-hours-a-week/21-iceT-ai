import streamlit as st
import httpx
import uuid
import pandas as pd
from datetime import datetime
from pathlib import Path

BASE_URL = "http://localhost:8000/api/ai/v2"

# CSV 경로
session_csv = Path("DB/chat_session.csv")
record_csv = Path("DB/chat_record.csv")
summary_csv = Path("DB/chat_summary.csv")

def append_csv(path, data):
    df = pd.DataFrame([data])
    if path.exists():
        df.to_csv(path, mode='a', index=False, header=False)
    else:
        df.to_csv(path, index=False)

# UI 구성
st.set_page_config(page_title="KocoAI", layout="centered")
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
        problem_number = st.number_input("문제 번호", value=9251, step=1)
    with col2:
        title = st.text_input("문제 제목", value="LCS")

    description = st.text_area("문제 설명", value=(
        "LCS(Longest Common Subsequence, 최장 공통 부분 수열) 문제는 두 수열이 주어졌을 때, "
        "모두의 부분 수열이 되는 수열 중 가장 긴 것을 찾는 문제이다. "
        "예를 들어 ACAYKP와 CAPCAK의 LCS는 ACAK가 된다."
    ), height=130)

    input_rule = st.text_area("입력 조건", value=(
        "첫째 줄과 둘째 줄에 각각 두 문자열이 주어진다. "
        "문자열은 알파벳 대문자로 이루어져 있으며, 최대 1000글자이다."
    ), height=80)

    output_rule = st.text_area("출력 조건", value=(
        "첫째 줄에 입력된 두 문자열의 LCS의 길이를 출력한다."
    ), height=80)

    input_example = st.text_input("입력 예시", value="ACAYKP\nCAPCAK")
    output_example = st.text_input("출력 예시", value="4")

    code = st.text_area("사용자 제출 코드", value=(
        'a = input().strip()\n'
        'b = input().strip()\n'
        'dp = [[0] * (len(b)+1) for _ in range(len(a)+1)]\n\n'
        'for i in range(1, len(a)+1):\n'
        '    for j in range(1, len(b)+1):\n'
        '        if a[i-1] == b[j-1]:\n'
        '            dp[i][j] = dp[i-1][j-1] + 1\n'
        '        else:\n'
        '            dp[i][j] = max(dp[i-1][j], dp[i][j-1])\n\n'
        'print(dp[len(a)][len(b)])'
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

    # ✅ 개선된 코드 마크다운 블록 감싸기
    improved_code = response.get("improvedCode", "").strip()
    language = st.session_state.start_payload.get("codeLanguage", "python")
    if not improved_code.startswith("```"):
        improved_code = f"```{language}\n{improved_code}\n```"

    # ✅ 어시스턴트 메시지 포맷
    if st.session_state.mode == "feedback":
        assistant_msg = (
            f"**✅ 잘한 점**\n" +
            "\n".join(f"- {item}" for item in response.get("good", [])) +
            "\n\n**⚠️ 개선할 점**\n" +
            "\n".join(f"- {item}" for item in response.get("bad", [])) +
            f"\n\n**🔧 개선된 코드**\n\n{improved_code}"
        )
    else:
        assistant_msg = response.get("question", "")


    user_msg = (
        f"📘 **문제 제목**: {title}\n\n"
        f"📝 **문제 설명**:\n{description}\n\n"
        f"🔢 **입력 조건**:\n{input_rule}\n"
        f"🔢 **출력 조건**:\n{output_rule}\n"
        f"🧪 **입출력 예시**:\n입력: {input_example}\n출력: {output_example}\n\n"
        f"💻 **사용자 코드 ({language})**:\n```{language}\n{code}\n```"
    )

    st.session_state.messages = [
        { "role": "user", "content": user_msg },
        { "role": "assistant", "content": assistant_msg }
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