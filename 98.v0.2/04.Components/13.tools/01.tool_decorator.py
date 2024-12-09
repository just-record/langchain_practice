from langchain_core.tools import tool


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


# Let's inspect some of the attributes associated with the tool.
### 1. tool과 관련된 속성들을 확인
print(f'name: {multiply.name}')
# name: multiply
print(f'description: {multiply.description}')
# description: Multiply two numbers.
print(f'args: {multiply.args}')
# args: {'a': {'title': 'A', 'type': 'integer'}, 'b': {'title': 'B', 'type': 'integer'}}


### 2. 비동기 구현
print('-'*30)
@tool
async def amultiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

print(f'name: {amultiply.name}')
# name: amultiply
print(f'description: {amultiply.description}')
# description: Multiply two numbers.
print(f'args: {amultiply.args}')
# args: {'a': {'title': 'A', 'type': 'integer'}, 'b': {'title': 'B', 'type': 'integer'}}


### 3. 사용자 정의 - tool name, JSON args
print('-'*30)
from langchain.pydantic_v1 import BaseModel, Field


class CalculatorInput(BaseModel):
    a: int = Field(description="first number")
    b: int = Field(description="second number")


@tool("multiplication-tool", args_schema=CalculatorInput, return_direct=True)
def cmultiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


print(f'name: {cmultiply.name}')
# name: multiplication-tool
print(f'description: {cmultiply.description}')
# description: Multiply two numbers.
print(f'args: {cmultiply.args}')
# args: {'a': {'title': 'A', 'description': 'first number', 'type': 'integer'}, 'b': {'title': 'B', 'description': 'second number', 'type': 'integer'}}
print(f'return_direct: {cmultiply.return_direct}')
# return_direct: True
