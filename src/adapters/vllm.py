# FIXME: 코드 완성 및 테스트 필요하나 해설 기능에는 vllm 사용 안할 것 같음

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

