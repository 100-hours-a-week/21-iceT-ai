from pydantic import BaseModel, Field

# api/v1/solution

# request
class SolutionRequest(BaseModel):
    problem_number: int
    title: str
    description: str
    input: str
    output: str
    input_example: str
    output_example: str
    language: str

# response
class ProblemCheck(BaseModel):
    problem_description: str = Field(description="요약된 문제 개요")
    algorithm: str = Field(description="사용된 알고리즘 종류")

class SolutionCode(BaseModel):
    python: str = Field(description="Python 코드")
    cpp: str = Field(description="C++ 코드")
    java: str = Field(description="Java 코드")

class SolutionResponse(BaseModel):
    problem_number: int = Field(description="문제 번호")
    problem_check: ProblemCheck = Field(description="문제 개요 및 알고리즘 설명")
    problem_solving: str = Field(description="단계별 구체적인 문제 풀이 방법")
    solution_code: SolutionCode = Field(description="python, c++, java 정답 코드")

