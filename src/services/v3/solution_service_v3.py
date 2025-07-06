import os, pickle
import logging
from langsmith import traceable
from src.schemas.v2.solution_schema_v2 import SolutionRequest, SolutionResponse
from src.core.v2.prompt_templates_v2 import SOLUTION_PROMPT
from src.adapters.v2.llm_client_v2 import generate_solution

logger = logging.getLogger(__name__)

# BM25Retriever
INDEX_SAVE_PATH = os.getenv("VECTOR_STORE_PATH")
with open(os.path.join(INDEX_SAVE_PATH, "bm25_index.pkl"), "rb") as f:
    bm25 = pickle.load(f)

# 문서 검색 함수
@traceable(run_type="retriever")
async def retrieve_docs(query: str):
    return bm25.get_relevant_documents(query)

# 문제 요청을 기반으로 해설 생성하는 서비스 함수
@traceable
async def explain_solution(req: SolutionRequest) -> SolutionResponse:
    query = " ".join(req.algorithm)
    docs  = await retrieve_docs(query)

    contexts = []
    for hit in docs[:4]:
        source = hit.metadata["source"]
        try:
            with open(source, encoding="utf-8") as f:
                contexts.append(f.read())
        except FileNotFoundError:
            continue

    context = "\n\n".join(contexts)

    prompt = SOLUTION_PROMPT.invoke({
        "problem_number": req.problem_number,
        "title":          req.title,
        "description":    req.description,
        "input":          req.input,
        "output":         req.output,
        "input_example":  req.input_example,
        "output_example": req.output_example,
        "context":        context,
    })

    return generate_solution(prompt.text)