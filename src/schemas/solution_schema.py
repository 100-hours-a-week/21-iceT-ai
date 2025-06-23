from pydantic import BaseModel, Field

class SolutionRequest(BaseModel):
    problemNumber: int = Field(description="문제 번호")
    title: str = Field(description="문제 제목")
    description: str = Field(description="문제 설명")
    input: str = Field(description="입력 설명")
    output: str = Field(description="출력 설명")
    inputExample: str = Field(description="입력 예시")
    outputExample: str = Field(description="출력 예시")

class ProblemCheck(BaseModel):
    problemDescription: str = Field(description="요약된 문제 개요", alias="problem_description")
    algorithm: str = Field(description="알고리즘 방법론", alias="algorithm")

class SolutionCode(BaseModel):
    python: str = Field(description="Python 코드")
    cpp: str = Field(description="C++ 코드")
    java: str = Field(description="Java 코드")

class SolutionResponse(BaseModel):
    problemNumber: int = Field(description="문제 번호")
    problemCheck: ProblemCheck = Field(description="문제 개요 및 알고리즘 설명", alias="problem_check")
    problemSolving: str = Field(description="문제 풀이 방법", alias="problem_solving")
    solutionCode: SolutionCode = Field(description="python, c++, java 정답 코드", alias="solution_code")