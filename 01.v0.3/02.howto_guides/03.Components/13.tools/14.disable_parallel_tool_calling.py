from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

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
llm = ChatOpenAI(model="gpt-4o-mini")


#################################################################################
### 1. 도구 호출은 기본적으로 병렬로 실행됨
### 'parallel_tool_call'을 사용 하여 단일 도구를 실행
print('1.', '-' * 50)
################################################################################## 
llm_with_tools = llm.bind_tools(tools)
rprint(llm_with_tools.invoke("Please call the first tool two times").tool_calls)
# 1. --------------------------------------------------
# [{'name': 'add', 'args': {'a': 1, 'b': 2}, 'id': 'call_JmvLQmuXXcYqeNN3NOWag0OS', 'type': 'tool_call'}, {'name': 'add', 'args': {'a': 3, 'b': 4}, 'id': 'call_Pha1LaiffvOvz1dWqaHa5Gpc', 'type': 'tool_call'}]

print(' ')
llm_with_tools = llm.bind_tools(tools, parallel_tool_calls=False)
rprint(llm_with_tools.invoke("Please call the first tool two times").tool_calls)
# [{'name': 'add', 'args': {'a': 1, 'b': 2}, 'id': 'call_Ljkrcuo0gyFgEvQi1UlgwMAp', 'type': 'tool_call'}]
