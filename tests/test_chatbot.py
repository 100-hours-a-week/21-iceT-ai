import gradio as gr
import asyncio
import httpx
import uuid

with gr.Blocks() as demo:
    gr.Markdown("## 💬 챗봇 테스트 Gradio")

    session_id = gr.State("")
    chat_history = gr.State([])

    mode_selector = gr.Radio(
        choices=["feedback", "interview"],
        value="feedback",
        label="💡 모드 선택"
    )

    # 문제 정보 입력
    with gr.Row():
        title = gr.Textbox(label="문제 제목", value="A + B")
        language = gr.Dropdown(choices=["python", "cpp", "java"], value="python", label="코드 언어")

    description = gr.Textbox(label="문제 설명", value="두 정수 A와 B를 입력받아 출력하는 문제")
    input_desc = gr.Textbox(label="입력 설명", value="두 정수 A, B (0 < A, B < 10)")
    output_desc = gr.Textbox(label="출력 설명", value="A + B 출력")
    input_ex = gr.Textbox(label="입력 예시", value="1 2")
    output_ex = gr.Textbox(label="출력 예시", value="3")
    code = gr.Code(label="사용자 코드", value="a, b = map(int, input().split())\nprint(a + b)")
    mode = gr.State("feedback")

    start_btn = gr.Button("Start")
    output_box = gr.Markdown(label="📨 첫 피드백 응답")

    followup_input = gr.Textbox(label="후속 질문")
    followup_btn = gr.Button("질문하기")
    followup_output = gr.Markdown(label="📨 후속 응답")

    # 💡 전체 히스토리 시각화 (추가 권장)
    chat_display = gr.Markdown(label="🧾 대화 히스토리")

    async def start_chat(
        title, description, input_desc, output_desc, input_ex, output_ex, language, code, mode_value
    ):
        output = ""
        session_id = str(uuid.uuid4())

        payload = {
            "sessionId": session_id,
            "problemNumber": 1000,
            "title": title,
            "description": description,
            "inputDescription": input_desc,
            "outputDescription": output_desc,
            "inputExample": input_ex,
            "outputExample": output_ex,
            "codeLanguage": language,
            "code": code,
        }

        url = (
        "http://localhost:8000/api/ai/v2/feedback/start"
        if mode_value == "feedback"
        else "http://localhost:8000/api/ai/v2/interview/start"
    )
        
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("POST", url, json=payload) as response:
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        content = line.replace("data: ", "")
                        output += content
                        yield gr.update(value=output), gr.update(), gr.update()

        # 🟢 스트리밍 종료 후 최종 3개 값 완성해서 한번 더 반환
        final_history = [
            {"role": "user", "content": code},
            {"role": "assistant", "content": output}
        ]
        yield gr.update(value=output), final_history, session_id

    start_btn.click(
        start_chat,
        inputs=[title, description, input_desc, output_desc, input_ex, output_ex, language, code, mode_selector],
        outputs=[output_box, chat_history, session_id]
    )

    async def answer_chat(user_msg, history, session_id, mode_value):
        if not session_id:
            yield "먼저 Start를 눌러 세션을 시작하세요.", history, session_id
            return

        # 메시지 누적
        history.append({"role": "user", "content": user_msg})

        payload = {
            "sessionId": session_id,
            "messages": history,
            "summary": None  # 요약은 생략
        }

        url = (
            "http://localhost:8000/api/ai/v2/feedback/answer"
            if mode_value == "feedback"
            else "http://localhost:8000/api/ai/v2/interview/answer"
        )

        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("POST", url, json=payload) as response:
                output = ""
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        content = line.replace("data: ", "")
                        output += content
                        yield output, history + [{"role": "assistant", "content": output}], session_id

    followup_btn.click(
        answer_chat,
        inputs=[followup_input, chat_history, session_id, mode_selector],
        outputs=[followup_output, chat_history, session_id]
    )

    # 💬 대화 히스토리 실시간 표시
    def render_chat(history):  # history: List[Dict]
        return "\n\n".join([f"**{m['role']}**: {m['content']}" for m in history])

    chat_history.change(render_chat, inputs=chat_history, outputs=chat_display)


if __name__ == "__main__":
    demo.launch()
