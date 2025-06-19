from pydantic import BaseModel, Field

# 요청 스키마
class SolutionRequest(BaseModel):
    problemNumber: int = Field(description="문제 번호")
    title: str = Field(description="문제 제목")
    description: str = Field(description="문제 설명")
    input: str = Field(description="입력 설명")
    output: str = Field(description="출력 설명")
    inputExample: str = Field(description="입력 예시")
    outputExample: str = Field(description="출력 예시")

# 내부 응답 구조
class ProblemCheck(BaseModel):
    problemDescription: str = Field(description="요약된 문제 개요", alias="problem_description")
    algorithm: str = Field(description="사용된 알고리즘 종류", alias="algorithm")

    model_config = {
        "populate_by_name": True
    }

class SolutionCode(BaseModel):
    python: str = Field(description="Python 코드", alias="python")
    cpp: str = Field(description="C++ 코드", alias="cpp")
    java: str = Field(description="Java 코드", alias="java")

    model_config = {
        "populate_by_name": True
    }

# 전체 응답 스키마
class SolutionResponse(BaseModel):
    problemNumber: int = Field(description="문제 번호", alias="problemNumber")
    problemCheck: ProblemCheck = Field(description="문제 개요 및 알고리즘 설명", alias="problem_check")
    problemSolving: str = Field(description="단계별 구체적인 문제 풀이 방법", alias="problem_solving")
    solutionCode: SolutionCode = Field(description="python, c++, java 정답 코드", alias="solution_code")

    model_config = {
        "populate_by_name": True
    }