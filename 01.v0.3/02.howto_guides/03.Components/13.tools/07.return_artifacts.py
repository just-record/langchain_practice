# 때로는 도구 실행의 결과물을 체인이나 에이전트의 하위 컴포넌트에서 접근 가능하게 하면서도, 모델 자체에는 노출하고 싶지 않을 수 있습니다. 
# 예를 들어 도구가 Documents와 같은 커스텀 객체를 반환할 때, 우리는 이 출력의 원시 데이터를 모델에 전달하지 않고 출력에 대한 뷰나 메타데이터만 모델에 전달하고 싶을 수 있습니다. 
# 동시에 다운스트림 도구와 같은 다른 곳에서 이 전체 출력에 접근할 수 있기를 원할 수 있습니다.

# Tool과 ToolMessage 인터페이스를 통해 모델을 위한 도구 출력 부분(이것이 ToolMessage.content입니다)과 모델 외부에서 사용하기 위한 부분(ToolMessage.artifact)을 구분할 수 있습니다.

# 도구가 메시지 내용과 다른 아티팩트를 구분하도록 하려면, 도구를 정의할 때 response_format="content_and_artifact"를 지정하고 (content, artifact) 튜플을 반환하도록 해야 합니다.


from rich import print as rprint
import random
from typing import List, Tuple

from langchain_core.tools import tool


#################################################################################
### 1. @tool -> response_format="content_and_artifact" 사용하여 content와 artifact 반환
### tool arguments만으로 tool을 바로 호출 하면 content만 반환
### content: ToolMessage.content(모델을 위한 도구 출력 부분)
### artifact: ToolMessage.artifact(모델 외부에서 사용할 수 있는 부분)
print('1.', '-' * 50)
################################################################################## 
@tool(response_format="content_and_artifact")
def generate_random_ints(min: int, max: int, size: int) -> Tuple[str, List[int]]:
    """Generate size random ints in the range [min, max]."""
    array = [random.randint(min, max) for _ in range(size)]
    content = f"Successfully generated array of {size} random ints in [{min}, {max}]."
    return content, array


rprint(generate_random_ints.invoke({"min": 0, "max": 9, "size": 10}))
# Successfully generated array of 10 random ints in [0, 9].


#################################################################################
### 2. @tool -> response_format="content_and_artifact" 사용하여 content와 artifact 반환
### ToolCall(ex: tool-calling models에 의해 생성된)로 tool을 호출 하면 content와 artifact 반환
### content: ToolMessage.content(모델을 위한 도구 출력 부분)
### artifact: ToolMessage.artifact(모델 외부에서 사용할 수 있는 부분)
print('2.', '-' * 50)
################################################################################## 
results = generate_random_ints.invoke(
    {
        "name": "generate_random_ints",
        "args": {"min": 0, "max": 9, "size": 10},
        "id": "123",  # required
        "type": "tool_call",  # required
    }
)
rprint(results)
# 2. --------------------------------------------------
# ToolMessage(content='Successfully generated array of 10 random ints in [0, 9].', name='generate_random_ints', tool_call_id='123', artifact=[6, 7, 9, 5, 7, 2, 5, 9, 5, 0])


#################################################################################
### 3. BaseTool을 상속받아서 구현
print('3.', '-' * 50)
################################################################################## 
from langchain_core.tools import BaseTool


class GenerateRandomFloats(BaseTool):
    name: str = "generate_random_floats"
    description: str = "Generate size random floats in the range [min, max]."
    response_format: str = "content_and_artifact"

    ndigits: int = 2

    def _run(self, min: float, max: float, size: int) -> Tuple[str, List[float]]:
        range_ = max - min
        array = [
            round(min + (range_ * random.random()), ndigits=self.ndigits)
            for _ in range(size)
        ]
        content = f"Generated {size} floats in [{min}, {max}], rounded to {self.ndigits} decimals."
        return content, array

    # Optionally define an equivalent async method

    # async def _arun(self, min: float, max: float, size: int) -> Tuple[str, List[float]]:
    #     ...
    
    
rand_gen = GenerateRandomFloats(ndigits=4)

results = rand_gen.invoke(
    {
        "name": "generate_random_floats",
        "args": {"min": 0.1, "max": 3.3333, "size": 3},
        "id": "123",
        "type": "tool_call",
    }
)
rprint(results)
# 3. --------------------------------------------------
# ToolMessage(content='Generated 3 floats in [0.1, 3.3333], rounded to 4 decimals.', name='generate_random_floats', tool_call_id='123', artifact=[0.4344, 2.5462, 1.0514])