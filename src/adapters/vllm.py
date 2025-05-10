# src/adapters/vllm.py

from vllm import LLM, SamplingParams

# 모델은 서버 시작 시 1회 로딩
llm = LLM(model="Qwen/Qwen2.5-Coder-7B-Instruct")
sampling_params = SamplingParams(temperature=0.3, max_tokens=1024)

def generate(prompt: str) -> str:
    outputs = llm.generate(prompt, sampling_params)
    return outputs[0].outputs[0].text.strip()
