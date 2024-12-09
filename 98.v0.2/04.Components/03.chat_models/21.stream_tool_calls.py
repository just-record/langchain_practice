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


llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
llm_with_tools = llm.bind_tools(tools)


### 1. 기본 사용법
query = "What is 3 * 12? Also, what is 11 + 49?"

async def chat_astream():
    async for chunk in llm_with_tools.astream(query):
        print(chunk.tool_call_chunks)

import asyncio
asyncio.run(chat_astream())   
# []
# [{'name': 'multiply', 'args': '', 'id': 'call_2qZBhJpdz5dqYldIHZncZ4u2', 'index': 0}]
# [{'name': None, 'args': '{"a"', 'id': None, 'index': 0}]
# [{'name': None, 'args': ': 3, ', 'id': None, 'index': 0}]
# [{'name': None, 'args': '"b": 1', 'id': None, 'index': 0}]
# [{'name': None, 'args': '2}', 'id': None, 'index': 0}]
# [{'name': 'add', 'args': '', 'id': 'call_LXHBHTciUby96atQyBnNe06U', 'index': 1}]
# [{'name': None, 'args': '{"a"', 'id': None, 'index': 1}]
# [{'name': None, 'args': ': 11,', 'id': None, 'index': 1}]
# [{'name': None, 'args': ' "b": ', 'id': None, 'index': 1}]
# [{'name': None, 'args': '49}', 'id': None, 'index': 1}]
# []     


### 2. chunk를 축적하기
print('-'*30)
async def chat_astream_accum():
    first = True
    async for chunk in llm_with_tools.astream(query):
        if first:
            gathered = chunk
            first = False
        else:
            gathered = gathered + chunk

        print(gathered.tool_call_chunks)

asyncio.run(chat_astream_accum()) 
# []
# [{'name': 'multiply', 'args': '', 'id': 'call_rKjvqqbNPHin1z7KUVnFKY73', 'index': 0}]
# [{'name': 'multiply', 'args': '{"a"', 'id': 'call_rKjvqqbNPHin1z7KUVnFKY73', 'index': 0}]
# [{'name': 'multiply', 'args': '{"a": 3, ', 'id': 'call_rKjvqqbNPHin1z7KUVnFKY73', 'index': 0}]
# [{'name': 'multiply', 'args': '{"a": 3, "b": 1', 'id': 'call_rKjvqqbNPHin1z7KUVnFKY73', 'index': 0}]
# [{'name': 'multiply', 'args': '{"a": 3, "b": 12}', 'id': 'call_rKjvqqbNPHin1z7KUVnFKY73', 'index': 0}]
# [{'name': 'multiply', 'args': '{"a": 3, "b": 12}', 'id': 'call_rKjvqqbNPHin1z7KUVnFKY73', 'index': 0}, {'name': 'add', 'args': '', 'id': 'call_I4SCjiAfqyQdZYG2TiSn8uGe', 'index': 1}]
# [{'name': 'multiply', 'args': '{"a": 3, "b": 12}', 'id': 'call_rKjvqqbNPHin1z7KUVnFKY73', 'index': 0}, {'name': 'add', 'args': '{"a"', 'id': 'call_I4SCjiAfqyQdZYG2TiSn8uGe', 'index': 1}]
# [{'name': 'multiply', 'args': '{"a": 3, "b": 12}', 'id': 'call_rKjvqqbNPHin1z7KUVnFKY73', 'index': 0}, {'name': 'add', 'args': '{"a": 11,', 'id': 'call_I4SCjiAfqyQdZYG2TiSn8uGe', 'index': 1}]
# [{'name': 'multiply', 'args': '{"a": 3, "b": 12}', 'id': 'call_rKjvqqbNPHin1z7KUVnFKY73', 'index': 0}, {'name': 'add', 'args': '{"a": 11, "b": ', 'id': 'call_I4SCjiAfqyQdZYG2TiSn8uGe', 'index': 1}]
# [{'name': 'multiply', 'args': '{"a": 3, "b": 12}', 'id': 'call_rKjvqqbNPHin1z7KUVnFKY73', 'index': 0}, {'name': 'add', 'args': '{"a": 11, "b": 49}', 'id': 'call_I4SCjiAfqyQdZYG2TiSn8uGe', 'index': 1}]
# [{'name': 'multiply', 'args': '{"a": 3, "b": 12}', 'id': 'call_rKjvqqbNPHin1z7KUVnFKY73', 'index': 0}, {'name': 'add', 'args': '{"a": 11, "b": 49}', 'id': 'call_I4SCjiAfqyQdZYG2TiSn8uGe', 'index': 1}]          


### 3. 파싱 부분을 시연하기
print('-'*30)
async def chat_astream_accum_parse():
    first = True
    async for chunk in llm_with_tools.astream(query):
        if first:
            gathered = chunk
            first = False
        else:
            gathered = gathered + chunk

        print(gathered.tool_calls)

asyncio.run(chat_astream_accum_parse()) 
# []
# []
# [{'name': 'multiply', 'args': {}, 'id': 'call_O7tkcJ8doUzySe86epxES8V4'}]
# [{'name': 'multiply', 'args': {'a': 3}, 'id': 'call_O7tkcJ8doUzySe86epxES8V4'}]
# [{'name': 'multiply', 'args': {'a': 3, 'b': 1}, 'id': 'call_O7tkcJ8doUzySe86epxES8V4'}]
# [{'name': 'multiply', 'args': {'a': 3, 'b': 12}, 'id': 'call_O7tkcJ8doUzySe86epxES8V4'}]
# [{'name': 'multiply', 'args': {'a': 3, 'b': 12}, 'id': 'call_O7tkcJ8doUzySe86epxES8V4'}]
# [{'name': 'multiply', 'args': {'a': 3, 'b': 12}, 'id': 'call_O7tkcJ8doUzySe86epxES8V4'}, {'name': 'add', 'args': {}, 'id': 'call_Z16UhEvJWLboDqUtzc7gPKMr'}]
# [{'name': 'multiply', 'args': {'a': 3, 'b': 12}, 'id': 'call_O7tkcJ8doUzySe86epxES8V4'}, {'name': 'add', 'args': {'a': 11}, 'id': 'call_Z16UhEvJWLboDqUtzc7gPKMr'}]
# [{'name': 'multiply', 'args': {'a': 3, 'b': 12}, 'id': 'call_O7tkcJ8doUzySe86epxES8V4'}, {'name': 'add', 'args': {'a': 11}, 'id': 'call_Z16UhEvJWLboDqUtzc7gPKMr'}]
# [{'name': 'multiply', 'args': {'a': 3, 'b': 12}, 'id': 'call_O7tkcJ8doUzySe86epxES8V4'}, {'name': 'add', 'args': {'a': 11, 'b': 49}, 'id': 'call_Z16UhEvJWLboDqUtzc7gPKMr'}]
# [{'name': 'multiply', 'args': {'a': 3, 'b': 12}, 'id': 'call_O7tkcJ8doUzySe86epxES8V4'}, {'name': 'add', 'args': {'a': 11, 'b': 49}, 'id': 'call_Z16UhEvJWLboDqUtzc7gPKMr'}]
