from langchain_core.tools import StructuredTool


def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


async def amultiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


### 1. 기본 사용법
calculator = StructuredTool.from_function(func=multiply, coroutine=amultiply)
# StructuredTool: 구조화된 입력을 받아 특정 작업을 수행하는 도구를 생성
# from_function(): 주어진 함수를 기반으로 StructuredTool 인스턴스를 생성
# func=multiply: 도구가 사용할 기본 동기 함수를 지정
# coroutine=amultiply: 도구가 사용할 비동기 함수(코루틴)를 지정

print(calculator.invoke({"a": 2, "b": 3}))
# 6

async def main():
    results = await calculator.ainvoke({"a": 2, "b": 5})
    print(results)

import asyncio
asyncio.run(main())
# 10

### 2. 추가 설정 하기
print('-'*30)
from langchain.pydantic_v1 import BaseModel, Field


class CalculatorInput(BaseModel):
    a: int = Field(description="first number")
    b: int = Field(description="second number")


def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


calculator = StructuredTool.from_function(
    func=multiply,
    name="Calculator",
    description="multiply numbers",
    args_schema=CalculatorInput,
    return_direct=True,
    # coroutine= ... <- you can specify an async method if desired as well
)

print(calculator.invoke({"a": 2, "b": 3}))
# 6
print(calculator.name)
# Calculator
print(calculator.description)
# multiply numbers
print(calculator.args)
# {'a': {'title': 'A', 'description': 'first number', 'type': 'integer'}, 'b': {'title': 'B', 'description': 'second number', 'type': 'integer'}}