from src.adapters.vllm import generate
from src.schemas.solution_schema import SolutionRequest, SolutionResponse
from src.core.prompt_templates import SOLUTION_PROMPT

async def explain_solution(req: SolutionRequest) -> SolutionResponse:
    prompt = SOLUTION_PROMPT.format(**req.model_dump())
    raw_output = generate(prompt)
    print("🧾 Qwen 응답 원본:\n", raw_output)

    try:
        sections = raw_output.split("문제 해결:")
        problem_check = sections[0].replace("문제 확인:", "").strip()

        rest = sections[1].split("코멘트:")
        problem_solving = rest[0].strip()

        comment_part = rest[1].split("정답 코드:")
        comment = comment_part[0].strip()

        code_block = comment_part[1].strip()
        solution_code = code_block.strip("`").split("\n", 1)[-1].strip()

        return SolutionResponse(
            problem_check=problem_check,
            problem_solving=problem_solving,
            comment=comment,
            solution_code=solution_code,
        )

    except Exception as e:
        raise ValueError(f"Qwen 응답 파싱 실패: {e}\n출력:\n{raw_output}")