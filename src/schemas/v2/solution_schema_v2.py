from pydantic import BaseModel, Field

# api/v1/solution

# request
class SolutionRequest(BaseModel):
    problem_number: int  = Field(description="문제 번호")
    title: str           = Field(description="문제 제목")
    description: str     = Field(description="문제 설명")
    input: str           = Field(description="입력 설명")
    output: str          = Field(description="출력 설명")
    input_example: str   = Field(description="입력 예시")
    output_example: str  = Field(description="출력 예시")
    algorithm: list[str] = Field(description="알고리즘 분류")

# response 중 문제 개요 및 알고리즘 설명
class ProblemCheck(BaseModel):
    problem_description: str = Field(description="문제 목표와 조건을 요약")
    algorithm: str = Field(description="사용된 알고리즘 종류, 정의, 작동 방법, 시간복잡도를 포함한 내용을 줄글로 설명")

# response 중 언어별 정답 코드
class SolutionCode(BaseModel):
    python: str = Field(description="Python 코드")
    cpp: str = Field(description="C++ 코드")
    java: str = Field(description="Java 코드")

# 전체 응답 스키마
class SolutionResponse(BaseModel):
    problemNumber: int = Field(description="문제 번호")
    problem_check: ProblemCheck = Field(description="문제 개요 및 알고리즘")
    problem_solving: str = Field(description="문제 풀이 방법을 단계별로 절차 설명")
    solution_code: SolutionCode = Field(description="python, c++, java 정답 코드")

