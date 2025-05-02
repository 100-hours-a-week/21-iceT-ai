# 크롤링 dict -> SolutionRequest 변환

from src.schemas.solution_schema import SolutionRequest

def to_solution_request(problem_data: dict, language="python") -> SolutionRequest:
    return SolutionRequest(
        problem_number=problem_data["problem_number"],
        title=problem_data["title"],
        description=problem_data["description"],
        input=problem_data["input"],
        output=problem_data["output"],
        input_example=problem_data["input_example"][0],
        output_example=problem_data["output_example"][0],
    )