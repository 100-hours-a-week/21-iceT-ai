from pydantic import BaseModel, Field

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
    problem_description: str = Field(description="요약된 문제 개요")
    algorithm: str = Field(description="사용된 알고리즘 종류")

class SolutionResponse(BaseModel):
    language: str = Field(description="사용된 언어명")
    problem_check: ProblemCheck = Field(description="문제 개요 및 알고리즘 설명")
    problem_solving: str = Field(description="단계별 구체적인 문제 풀이 방법")
    solution_code: str = Field(description="정답 코드")