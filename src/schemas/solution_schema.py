from pydantic import BaseModel, Field

# api/v1/solution

# request
class SolutionRequest(BaseModel):
<<<<<<< HEAD
    problem_number: int
    title: str
    description: str
    input: str
    output: str
    input_example: str
    output_example: str

# response
=======
    problem_number: int  # 문제 번호
    title: str           # 문제 제목
    description: str     # 문제 설명
    input: str           # 입력 설명
    output: str          # 출력 설명
    input_example: str   # 입력 예시
    output_example: str  # 출력 예시

# response 중 문제 개요 및 알고리즘 설명
>>>>>>> origin/dev
class ProblemCheck(BaseModel):
    problem_description: str = Field(description="요약된 문제 개요")
    algorithm: str = Field(description="사용된 알고리즘 종류")

<<<<<<< HEAD
=======
# response 중 언어별 정답 코드
>>>>>>> origin/dev
class SolutionCode(BaseModel):
    python: str = Field(description="Python 코드")
    cpp: str = Field(description="C++ 코드")
    java: str = Field(description="Java 코드")

<<<<<<< HEAD
class SolutionResponse(BaseModel):
    problem_number: int = Field(description="문제 번호")
=======
# 전체 응답 스키마
class SolutionResponse(BaseModel):
    problemNumber: int = Field(description="문제 번호")
>>>>>>> origin/dev
    problem_check: ProblemCheck = Field(description="문제 개요 및 알고리즘 설명")
    problem_solving: str = Field(description="단계별 구체적인 문제 풀이 방법")
    solution_code: SolutionCode = Field(description="python, c++, java 정답 코드")

