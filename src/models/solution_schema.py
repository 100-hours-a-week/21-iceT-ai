from pydantic import BaseModel

# api/v1/solution

# request
class SolutionRequest(BaseModel):
    problem_number: int
    title: str
    description: str
    input_example: str
    output_example: str
    language: str

# response
class ProblemCheck(BaseModel):
    problem_description: str
    algorithm: str

# response
class SolutionResponse(BaseModel):
    language: str
    problem_check: ProblemCheck
    problem_solving: str
    solution_code: str