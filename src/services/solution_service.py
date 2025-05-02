from src.core.prompt_templates import SOLUTION_PROMPT
from src.adapters.llm_client import generate_solution
from src.schemas.solution_schema import SolutionRequest, SolutionResponse

async def explain_solution(req: SolutionRequest) -> SolutionResponse:
    prompt = SOLUTION_PROMPT.invoke(
        {
            "problem_number": req.problem_number,
            "title":          req.title,
            "description":    req.description,
            "input":          req.input,
            "output":         req.output,
            "input_example":  req.input_example,
            "output_example": req.output_example
        }
    )
    result = generate_solution(prompt)
    return result