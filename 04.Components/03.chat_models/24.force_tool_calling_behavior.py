from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool


@tool
def add(a: int, b: int) -> int:
    """Adds a and b."""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiplies a and b."""
    return a * b


tools = [add, multiply]

llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

### 1. 무조건 특정 도구를 호출 하도록 강제하기 - tool_choice="Multiply"
llm_forced_to_multiply = llm.bind_tools(tools, tool_choice="multiply")
results = llm_forced_to_multiply.invoke("what is 2 + 4")
print(results.tool_calls)
# [{'name': 'multiply', 'args': {'a': 2, 'b': 4}, 'id': 'call_OgwOASURMFpa1pdh8z0Q5den'}]


### 2. 무조건 도구 중 하나를 호출 하도록 강제하기 - tool_choice="any"
print('-'*30)
llm_forced_to_use_tool = llm.bind_tools(tools, tool_choice="any")
results = llm_forced_to_use_tool.invoke("What day is today?")
print(results.tool_calls)
# [{'name': 'add', 'args': {'a': 1, 'b': 1}, 'id': 'call_SoJVyBIBFfRbF0KXkbxgCvTv'}]