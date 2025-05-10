<<<<<<< HEAD
# src/adapters/vllm.py

from vllm import LLM, SamplingParams

# 모델은 서버 시작 시 1회 로딩
llm = LLM(model="Qwen/Qwen2.5-Coder-7B-Instruct")
sampling_params = SamplingParams(temperature=0.3, max_tokens=1024)

def generate(prompt: str) -> str:
    outputs = llm.generate(prompt, sampling_params)
    return outputs[0].outputs[0].text.strip()
=======
# TODO: 코드 완성 및 테스트 필요

####################################################################################
# vLLM 서버 실행 (OpenAI-호환 모드)
####################################################################################
# vllm serve \
#   --model-path ${YOUR_MODEL_PATH} \
#   --openai-compatible \
#   --port 8001


from langchain_community.llms import VLLMOpenAI
from src.config import settings
from dotenv import load_dotenv
from src.schemas.solution_schema import SolutionResponse

load_dotenv()

# OpenAI-호환 엔드포인트로 VLLM 클라이언트 생성
vllm_llm = VLLMOpenAI(
    openai_api_key="EMPTY",                      # vLLM 서버는 키 검증을 하지 않으니 더미값 OK
    openai_api_base="http://localhost:8001/v1",  # 위에서 띄운 서버의 /v1 엔드포인트
    model_name=settings.model,
    model_kwargs={
        "temperature": settings.temperature,
        "max_tokens": settings.max_tokens,
        "top_p": 0.9,
    },
)

structured_llm = vllm_llm.with_structured_output(SolutionResponse)

def generate_solution(prompt: str) -> SolutionResponse:
    result = structured_llm.ainvoke(prompt)
    return result

>>>>>>> origin/dev
