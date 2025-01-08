### https://python.langchain.com/docs/how_to/custom_tools/#how-to-create-async-tools 내용 확인

## 모든 Runnable은 invoke와 ainvoke 메서드를 제공합니다 (그 외 batch, abatch, astream 등도 포함).
## 주요 내용:
# 동기(sync) 구현만 제공하더라도 ainvoke 인터페이스를 사용할 수 있습니다
# LangChain은 기본적으로 함수가 계산 비용이 많이 든다고 가정하고 다른 스레드에서 실행하는 비동기 구현을 제공합니다
# 비동기 코드베이스에서 작업할 경우, 스레드 전환으로 인한 오버헤드를 피하기 위해 동기 도구 대신 비동기 도구를 만들어야 합니다
# 동기와 비동기 구현이 모두 필요한 경우 StructuredTool.from_function을 사용하거나 BaseTool을 상속받으세요
# 동기 코드가 빠르게 실행되는 경우, LangChain의 기본 비동기 구현을 재정의하고 동기 코드를 직접 호출하세요
# 비동기 도구에서 동기 invoke를 사용해서는 안 됩니다

from rich import print as rprint
from langchain_core.tools import StructuredTool


def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


#################################################################################
### 1. 동기만 정의하더라도 ainvoke 인터페이스 사용 가능
### 하지만 초기 스레드 생성으로 인한 작은 오버헤드 발생
print('1.', '-' * 50)
################################################################################## 
calculator = StructuredTool.from_function(func=multiply)

print(calculator.invoke({"a": 2, "b": 3}))

async def ainvoke_func() -> int:
    return await calculator.ainvoke({"a": 2, "b": 5})

import asyncio
rprint(asyncio.run(ainvoke_func()))
# 1. --------------------------------------------------
# 6
# 10


#################################################################################
### 2. 동기, 비동기 모두 정의하여 추가 오버헤드 없이 사용 가능
print('2.', '-' * 50)
################################################################################## 
from langchain_core.tools import StructuredTool


def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


async def amultiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


calculator = StructuredTool.from_function(func=multiply, coroutine=amultiply)

print(calculator.invoke({"a": 2, "b": 3}))
async def ainvoke_func() -> int:
    return await calculator.ainvoke({"a": 2, "b": 5})

import asyncio
rprint(asyncio.run(ainvoke_func()))
# 2. --------------------------------------------------
# 6
# 10


#################################################################################
### 3. 비동기만 정의하고 '.invoke()'를 사용하면 오류 발생
print('3.', '-' * 50)
################################################################################## 
from langchain_core.tools import tool


@tool
async def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


try:
    multiply.invoke({"a": 2, "b": 3})
except NotImplementedError:
    print("Raised not implemented error. You should not be doing this.")
# 3. --------------------------------------------------
# Raised not implemented error. You should not be doing this.    