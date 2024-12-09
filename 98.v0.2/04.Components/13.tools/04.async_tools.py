from langchain_core.tools import StructuredTool


def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


### 1. 비동기 설정 없이 사용
calculator = StructuredTool.from_function(func=multiply)

print(calculator.invoke({"a": 2, "b": 3}))
# 6

async def main():
    results = await calculator.ainvoke({"a": 2, "b": 5})
    print(results)

import asyncio
asyncio.run(main())
# 10


### 2. 비동기 설정 추가
print('-'*30)
from langchain_core.tools import StructuredTool


async def amultiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


calculator = StructuredTool.from_function(func=multiply, coroutine=amultiply)

print(calculator.invoke({"a": 2, "b": 3}))
asyncio.run(main())


### 3. 비동기를 invoke로 호출 하렴 error 발생
print('-'*30)

try:
    amultiply.invoke({"a": 2, "b": 3})
except Exception as e:
    print(f'Error: {e}')
# Error: 'function' object has no attribute 'invoke'    