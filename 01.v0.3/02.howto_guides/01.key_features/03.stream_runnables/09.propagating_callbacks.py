from langchain_core.runnables import RunnableLambda
from langchain_core.tools import tool


#################################################################################
### 1. 도구 호출 시 콜백을 전파하지 않으면 astream_events()가 생성되지 않음
### RunnableLambdas나 @chain 데코레이터를 사용할 때, 콜백들은 자동으로 백그라운드에서 전파됨
print('1.', '-' * 50)
##################################################################################
def reverse_word(word: str):
    return word[::-1]


reverse_word = RunnableLambda(reverse_word)


@tool
def bad_tool(word: str):
    """Custom tool that doesn't propagate callbacks."""
    return reverse_word.invoke(word)

import asyncio

async def astream_events_func():
    async for event in bad_tool.astream_events("hello", version="v2"):
        print(event)

asyncio.run(astream_events_func())
# 1. --------------------------------------------------
# {'event': 'on_tool_start', 'data': {'input': 'hello'}, 'name': 'bad_tool', 'tags': [], 'run_id': 'f6d77944-c914-4100-b258-312c50c3ac68', 'metadata': {}, 'parent_ids': []}
# {'event': 'on_chain_start', 'data': {'input': 'hello'}, 'name': 'reverse_word', 'tags': [], 'run_id': '3c631743-04d5-4f5c-affc-5a9617092449', 'metadata': {}, 'parent_ids': ['f6d77944-c914-4100-b258-312c50c3ac68']}
# {'event': 'on_chain_end', 'data': {'output': 'olleh', 'input': 'hello'}, 'run_id': '3c631743-04d5-4f5c-affc-5a9617092449', 'name': 'reverse_word', 'tags': [], 'metadata': {}, 'parent_ids': ['f6d77944-c914-4100-b258-312c50c3ac68']}
# {'event': 'on_tool_end', 'data': {'output': 'olleh'}, 'run_id': 'f6d77944-c914-4100-b258-312c50c3ac68', 'name': 'bad_tool', 'tags': [], 'metadata': {}, 'parent_ids': []}


#################################################################################
### 2. 도구 호출 시 콜백 전파
print('2.', '-' * 50)
##################################################################################
@tool
def correct_tool(word: str, callbacks):
    """A tool that correctly propagates callbacks."""
    return reverse_word.invoke(word, {"callbacks": callbacks})


async def astream_events_func():
    async for event in correct_tool.astream_events("hello", version="v2"):
        print(event)

asyncio.run(astream_events_func())
# 2. --------------------------------------------------
# {'event': 'on_tool_start', 'data': {'input': 'hello'}, 'name': 'correct_tool', 'tags': [], 'run_id': 'a04141be-3032-4538-afa3-894e015f887f', 'metadata': {}, 'parent_ids': []}
# {'event': 'on_chain_start', 'data': {'input': 'hello'}, 'name': 'reverse_word', 'tags': [], 'run_id': '486808f4-d588-4b36-93ef-788e18d07169', 'metadata': {}, 'parent_ids': ['a04141be-3032-4538-afa3-894e015f887f']}
# {'event': 'on_chain_end', 'data': {'output': 'olleh', 'input': 'hello'}, 'run_id': '486808f4-d588-4b36-93ef-788e18d07169', 'name': 'reverse_word', 'tags': [], 'metadata': {}, 'parent_ids': ['a04141be-3032-4538-afa3-894e015f887f']}
# {'event': 'on_tool_end', 'data': {'output': 'olleh'}, 'run_id': 'a04141be-3032-4538-afa3-894e015f887f', 'name': 'correct_tool', 'tags': [], 'metadata': {}, 'parent_ids': []}


#################################################################################
### 3. 
### Runnable Lambda나 @chains 내에서 runnable을 호출할 경우, callback들은 자동으로 전달
print('3.', '-' * 50)
##################################################################################
from langchain_core.runnables import RunnableLambda


async def reverse_and_double(word: str):
    return await reverse_word.ainvoke(word) * 2


reverse_and_double = RunnableLambda(reverse_and_double)


async def reverse_and_double_func(input_str: str) -> str:
    return await reverse_and_double.ainvoke(input_str)

results = asyncio.run(reverse_and_double_func("1234"))
print(results)
# 3. --------------------------------------------------
# 43214321

print(' ')
async def astream_events_func():
    async for event in reverse_and_double.astream_events("1234", version="v2"):
        print(event)
        
asyncio.run(astream_events_func())
# {'event': 'on_chain_start', 'data': {'input': '1234'}, 'name': 'reverse_and_double', 'tags': [], 'run_id': '36723266-96b4-4f10-bb1d-25e146f46cae', 'metadata': {}, 'parent_ids': []}
# {'event': 'on_chain_stream', 'run_id': '36723266-96b4-4f10-bb1d-25e146f46cae', 'name': 'reverse_and_double', 'tags': [], 'metadata': {}, 'data': {'chunk': '43214321'}, 'parent_ids': []}
# {'event': 'on_chain_end', 'data': {'output': '43214321'}, 'run_id': '36723266-96b4-4f10-bb1d-25e146f46cae', 'name': 'reverse_and_double', 'tags': [], 'metadata': {}, 'parent_ids': []}


#################################################################################
### 4. @chain 데코레이터 사용
print('4.', '-' * 50)
##################################################################################
from langchain_core.runnables import chain


@chain
async def reverse_and_double(word: str):
    return await reverse_word.ainvoke(word) * 2


async def reverse_and_double_func(input_str: str) -> str:
    return await reverse_and_double.ainvoke(input_str)

results = asyncio.run(reverse_and_double_func("1234"))
print(results)
# 4. --------------------------------------------------
# 43214321

print(' ')
async def astream_events_func():
    async for event in reverse_and_double.astream_events("1234", version="v2"):
        print(event)
        
asyncio.run(astream_events_func())
# {'event': 'on_chain_start', 'data': {'input': '1234'}, 'name': 'reverse_and_double', 'tags': [], 'run_id': '99a38d3a-ca4b-405e-bec2-f4aef9802c64', 'metadata': {}, 'parent_ids': []}
# {'event': 'on_chain_stream', 'run_id': '99a38d3a-ca4b-405e-bec2-f4aef9802c64', 'name': 'reverse_and_double', 'tags': [], 'metadata': {}, 'data': {'chunk': '43214321'}, 'parent_ids': []}
# {'event': 'on_chain_end', 'data': {'output': '43214321'}, 'run_id': '99a38d3a-ca4b-405e-bec2-f4aef9802c64', 'name': 'reverse_and_double', 'tags': [], 'metadata': {}, 'parent_ids': []}