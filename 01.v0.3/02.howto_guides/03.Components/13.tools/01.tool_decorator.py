from rich import print as rprint
from langchain_core.tools import tool


#################################################################################
### 1. @tool 을 사용하여 함수를 도구로 만들기
### function namd을 tool name으로 사용
### function의 docstring을 tool's description으로. docstring은 반드시 있어야 함
print('1.', '-' * 50)
##################################################################################
@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


# Let's inspect some of the attributes associated with the tool.
rprint(multiply.name)
rprint(multiply.description)
rprint(multiply.args)
# 1. --------------------------------------------------
# multiply
# Multiply two numbers.
# {'a': {'title': 'A', 'type': 'integer'}, 'b': {'title': 'B', 'type': 'integer'}}


#################################################################################
### 2. @tool - 비동기
print('2.', '-' * 50)
##################################################################################
@tool
async def amultiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


rprint(amultiply.name)
rprint(amultiply.description)
rprint(amultiply.args)
# 2. --------------------------------------------------
# amultiply
# Multiply two numbers.
# {'a': {'title': 'A', 'type': 'integer'}, 'b': {'title': 'B', 'type': 'integer'}}


#################################################################################
### 3. @tool - 어노테이션 파싱, 중첩된 스키마 및 기타 기능을 지원
print('3.', '-' * 50)
##################################################################################
from typing import Annotated, List


@tool
def multiply_by_max(
    a: Annotated[int, "scale factor"],
    b: Annotated[List[int], "list of ints over which to take maximum"],
) -> int:
    """Multiply a by the maximum of b."""
    return a * max(b)


# model_json_schema()는 Pydantic 모델의 JSON 스키마를 생성하는 메서드
rprint(multiply_by_max.args_schema.model_json_schema())
# 3. --------------------------------------------------
# {
#     'description': 'Multiply a by the maximum of b.',
#     'properties': {
#         'a': {'description': 'scale factor', 'title': 'A', 'type': 'integer'},
#         'b': {'description': 'list of ints over which to take maximum', 'items': {'type': 'integer'}, 'title': 'B', 'type': 'array'}
#     },
#     'required': ['a', 'b'],
#     'title': 'multiply_by_max',
#     'type': 'object'
# }


#################################################################################
### 4. @tool - tool name과 JSON args를 설정
### return_direct: bool
### True: 도구가 반환하는 결과를 LLM을 거치지 않고 직접적으로 최종 사용자에게 전달
### False: 도구의 출력이 LLM으로 다시 전달하여 LLM이 결과를 해석하고 필요한 경우 추가 처리
print('4.', '-' * 50)
##################################################################################
from pydantic import BaseModel, Field


class CalculatorInput(BaseModel):
    a: int = Field(description="first number")
    b: int = Field(description="second number")


@tool("multiplication-tool", args_schema=CalculatorInput, return_direct=True)
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


# Let's inspect some of the attributes associated with the tool.
rprint(multiply.name)
rprint(multiply.description)
rprint(multiply.args)
rprint(multiply.return_direct)
# 4. --------------------------------------------------
# multiplication-tool
# Multiply two numbers.
# {'a': {'description': 'first number', 'title': 'A', 'type': 'integer'}, 'b': {'description': 'second number', 'title': 'B', 'type': 'integer'}}
# True


#################################################################################
### 5. Docstring를 파싱하여 tool schema를 생성
### Google Style docstring
### 'parse_docstring' True로 설정
### docstring이 제대로 파싱되지 않으면 ValueError 발생
print('5.', '-' * 50)
##################################################################################
@tool(parse_docstring=True)
def foo(bar: str, baz: int) -> str:
    """The foo.

    Args:
        bar: The bar.
        baz: The baz.
    """
    return bar


rprint(foo.args_schema.model_json_schema())\
# 5. --------------------------------------------------
# {
#     'description': 'The foo.',
#     'properties': {'bar': {'description': 'The bar.', 'title': 'Bar', 'type': 'string'}, 'baz': {'description': 'The baz.', 'title': 'Baz', 'type': 'integer'}},
#     'required': ['bar', 'baz'],
#     'title': 'foo',
#     'type': 'object'
# }    