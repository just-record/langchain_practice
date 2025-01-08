# BaseTool을 상속받아 커스텀 도구를 정의할 수 있습니다. 
# 이 방법은 도구 정의에 대한 최대한의 제어를 제공하지만, 더 많은 코드를 작성해야 합니다.
from rich import print as rprint
from typing import Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class CalculatorInput(BaseModel):
    a: int = Field(description="first number")
    b: int = Field(description="second number")


# Note: It's important that every field has type hints. BaseTool is a
# Pydantic class and not having type hints can lead to unexpected behavior.
class CustomCalculatorTool(BaseTool):
    name: str = "Calculator"
    description: str = "useful for when you need to answer questions about math"
    args_schema: Type[BaseModel] = CalculatorInput
    return_direct: bool = True

    def _run(
        self, a: int, b: int, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        return a * b

    async def _arun(
        self,
        a: int,
        b: int,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        # If the calculation is cheap, you can just delegate to the sync implementation
        # as shown below.
        # If the sync calculation is expensive, you should delete the entire _arun method.
        # LangChain will automatically provide a better implementation that will
        # kick off the task in a thread to make sure it doesn't block other async code.
        return self._run(a, b, run_manager=run_manager.get_sync())
    
    
#################################################################################
### 1. CustomCalculatorTool - BaseTool을 상속받아 커스텀 도구를 정의 하는 예시
print('1.', '-' * 50)
##################################################################################    
multiply = CustomCalculatorTool()
print(multiply.name)
print(multiply.description)
print(multiply.args)
print(multiply.return_direct)

print(multiply.invoke({"a": 2, "b": 3}))
### 비동기 - ainvoke ###
async def multiply_ainvoke() -> int:
    return await multiply.ainvoke({"a": 2, "b": 3})

import asyncio
rprint(asyncio.run(multiply_ainvoke()))
# 1. --------------------------------------------------
# Calculator
# useful for when you need to answer questions about math
# {'a': {'description': 'first number', 'title': 'A', 'type': 'integer'}, 'b': {'description': 'second number', 'title': 'B', 'type': 'integer'}}
# True
# 6
# 6