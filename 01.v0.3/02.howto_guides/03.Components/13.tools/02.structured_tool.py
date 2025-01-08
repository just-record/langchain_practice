from rich import print as rprint
from pydantic import BaseModel, Field
from langchain_core.tools import StructuredTool


def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


async def amultiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


#################################################################################
### 1. StructuredTool.from_function
### @tool 보다 조금 더 설정이 가능한 도구 생성이 가능 - 조금 더 코드가 추가
print('1.', '-' * 50)
##################################################################################
calculator = StructuredTool.from_function(func=multiply, coroutine=amultiply)

rprint(calculator.invoke({"a": 2, "b": 3}))

### 비동기 - ainvoke ###
async def calculator_ainvoke() -> int:
    return await calculator.ainvoke({"a": 2, "b": 5})

import asyncio
rprint(asyncio.run(calculator_ainvoke()))
# 1. --------------------------------------------------
# 6
# 10


#################################################################################
### 2. StructuredTool.from_function - 설정하기
print('2.', '-' * 50)
##################################################################################
class CalculatorInput(BaseModel):
    a: int = Field(description="first number")
    b: int = Field(description="second number")


# def multiply(a: int, b: int) -> int:
#     """Multiply two numbers."""
#     return a * b


calculator = StructuredTool.from_function(
    func=multiply,
    name="Calculator",
    description="multiply numbers",
    args_schema=CalculatorInput,
    return_direct=True,
    # coroutine= ... <- you can specify an async method if desired as well
)

rprint(calculator.invoke({"a": 2, "b": 3}))
rprint(calculator.name)
rprint(calculator.description)
rprint(calculator.args)
# 2. --------------------------------------------------
# 6
# Calculator
# multiply numbers
# {'a': {'description': 'first number', 'title': 'A', 'type': 'integer'}, 'b': {'description': 'second number', 'title': 'B', 'type': 'integer'}}


#################################################################################
### 3. StructuredTool.from_function - 설정하기(비동기 포함)
print('3.', '-' * 50)
##################################################################################
calculator_sync_async = StructuredTool.from_function(
    func=multiply,
    coroutine=amultiply,
    name="Calculator",
    description="multiply numbers",
    args_schema=CalculatorInput,
    return_direct=True,
    # coroutine= ... <- you can specify an async method if desired as well
)

rprint(calculator_sync_async.invoke({"a": 2, "b": 3}))
rprint(calculator_sync_async.name)
rprint(calculator_sync_async.description)
rprint(calculator_sync_async.args)
rprint(calculator_sync_async.args_schema.model_json_schema())

### 비동기 - ainvoke ###
async def calculator_sync_async_ainvoke() -> int:
    return await calculator_sync_async.ainvoke({"a": 2, "b": 5})

import asyncio
rprint(asyncio.run(calculator_sync_async_ainvoke()))
# 3. --------------------------------------------------
# 6
# Calculator
# multiply numbers
# {'a': {'description': 'first number', 'title': 'A', 'type': 'integer'}, 'b': {'description': 'second number', 'title': 'B', 'type': 'integer'}}
# {
#     'properties': {'a': {'description': 'first number', 'title': 'A', 'type': 'integer'}, 'b': {'description': 'second number', 'title': 'B', 'type': 'integer'}},
#     'required': ['a', 'b'],
#     'title': 'CalculatorInput',
#     'type': 'object'
# }
# 10