from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

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



from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm_with_tools = llm.bind_tools(tools)


#################################################################################
### 1. tool call - stream
### tool_call_chunks: 도구 호출 청크 객체 목록
### => 도구 이름, 인수, ID에 대한 선택적 문자열 필드를 포함, 청크를 함께 결합하는 데 사용할 수 있는 선택적 정수 필드 인덱스도 포함
### 도구 호출의 일부가 서로 다른 청크에 걸쳐 스트리밍될 수 있기 때문에 필드는 선택사항
print('1.', '-' * 50)
##################################################################################
query = "What is 3 * 12? Also, what is 11 + 49?"

async def astream_func():
    async for chunk in llm_with_tools.astream(query):
        rprint(chunk.tool_call_chunks)

import asyncio
asyncio.run(astream_func())     
# 1. --------------------------------------------------
# []
# [{'name': 'multiply', 'args': '', 'id': 'call_pUD8OsvVDO9Q3TQZYOEs0Jag', 'index': 0, 'type': 'tool_call_chunk'}]
# [{'name': None, 'args': '{"a"', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
# [{'name': None, 'args': ': 3, ', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
# [{'name': None, 'args': '"b": 1', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
# [{'name': None, 'args': '2}', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
# [{'name': 'add', 'args': '', 'id': 'call_KWLcazZ0Y0KDX38lQgdblfkV', 'index': 1, 'type': 'tool_call_chunk'}]
# [{'name': None, 'args': '{"a"', 'id': None, 'index': 1, 'type': 'tool_call_chunk'}]
# [{'name': None, 'args': ': 11,', 'id': None, 'index': 1, 'type': 'tool_call_chunk'}]
# [{'name': None, 'args': ' "b": ', 'id': None, 'index': 1, 'type': 'tool_call_chunk'}]
# [{'name': None, 'args': '49}', 'id': None, 'index': 1, 'type': 'tool_call_chunk'}]
# []   


#################################################################################
### 2. tool_call_chunks 누적하기
print('2.', '-' * 50)
##################################################################################
async def astream_func():
    first = True
    async for chunk in llm_with_tools.astream(query):
        if first:
            gathered = chunk
            first = False
        else:
            gathered = gathered + chunk

        print(gathered.tool_call_chunks)
    return gathered
        
gathered = asyncio.run(astream_func())      
# 2. --------------------------------------------------
# []
# [{'name': 'multiply', 'args': '', 'id': 'call_UwTFeMDIbRq6R9S43rRvLS2u', 'index': 0, 'type': 'tool_call_chunk'}]
# [{'name': 'multiply', 'args': '{"a"', 'id': 'call_UwTFeMDIbRq6R9S43rRvLS2u', 'index': 0, 'type': 'tool_call_chunk'}]
# [{'name': 'multiply', 'args': '{"a": 3, ', 'id': 'call_UwTFeMDIbRq6R9S43rRvLS2u', 'index': 0, 'type': 'tool_call_chunk'}]
# [{'name': 'multiply', 'args': '{"a": 3, "b": 1', 'id': 'call_UwTFeMDIbRq6R9S43rRvLS2u', 'index': 0, 'type': 'tool_call_chunk'}]
# [{'name': 'multiply', 'args': '{"a": 3, "b": 12}', 'id': 'call_UwTFeMDIbRq6R9S43rRvLS2u', 'index': 0, 'type': 'tool_call_chunk'}]
# [{'name': 'multiply', 'args': '{"a": 3, "b": 12}', 'id': 'call_UwTFeMDIbRq6R9S43rRvLS2u', 'index': 0, 'type': 'tool_call_chunk'}, {'name': 'add', 'args': '', 'id': 'call_gcL1JViBeNeamyGP3EfqClWq', 'index': 1, 'type': 'tool_call_chunk'}]
# [{'name': 'multiply', 'args': '{"a": 3, "b": 12}', 'id': 'call_UwTFeMDIbRq6R9S43rRvLS2u', 'index': 0, 'type': 'tool_call_chunk'}, {'name': 'add', 'args': '{"a"', 'id': 'call_gcL1JViBeNeamyGP3EfqClWq', 'index': 1, 'type': 'tool_call_chunk'}]
# [{'name': 'multiply', 'args': '{"a": 3, "b": 12}', 'id': 'call_UwTFeMDIbRq6R9S43rRvLS2u', 'index': 0, 'type': 'tool_call_chunk'}, {'name': 'add', 'args': '{"a": 11,', 'id': 'call_gcL1JViBeNeamyGP3EfqClWq', 'index': 1, 'type': 'tool_call_chunk'}]
# [{'name': 'multiply', 'args': '{"a": 3, "b": 12}', 'id': 'call_UwTFeMDIbRq6R9S43rRvLS2u', 'index': 0, 'type': 'tool_call_chunk'}, {'name': 'add', 'args': '{"a": 11, "b": ', 'id': 'call_gcL1JViBeNeamyGP3EfqClWq', 'index': 1, 'type': 'tool_call_chunk'}]
# [{'name': 'multiply', 'args': '{"a": 3, "b": 12}', 'id': 'call_UwTFeMDIbRq6R9S43rRvLS2u', 'index': 0, 'type': 'tool_call_chunk'}, {'name': 'add', 'args': '{"a": 11, "b": 49}', 'id': 'call_gcL1JViBeNeamyGP3EfqClWq', 'index': 1, 'type': 'tool_call_chunk'}]
# [{'name': 'multiply', 'args': '{"a": 3, "b": 12}', 'id': 'call_UwTFeMDIbRq6R9S43rRvLS2u', 'index': 0, 'type': 'tool_call_chunk'}, {'name': 'add', 'args': '{"a": 11, "b": 49}', 'id': 'call_gcL1JViBeNeamyGP3EfqClWq', 'index': 1, 'type': 'tool_call_chunk'}]  

print(' ')
print(type(gathered.tool_call_chunks[0]["args"]))
# <class 'str'>


#################################################################################
### 3. 부분 파싱을 위한 도구 호출 누적
print('3.', '-' * 50)
##################################################################################
async def astream_func():
    first = True
    async for chunk in llm_with_tools.astream(query):
        if first:
            gathered = chunk
            first = False
        else:
            gathered = gathered + chunk

        print(gathered.tool_calls)
    return gathered
        
gathered = asyncio.run(astream_func())   
# 3. --------------------------------------------------
# []
# [{'name': 'multiply', 'args': {}, 'id': 'call_t7mPosFh2RJNjKbITMIJBHDx', 'type': 'tool_call'}]
# [{'name': 'multiply', 'args': {}, 'id': 'call_t7mPosFh2RJNjKbITMIJBHDx', 'type': 'tool_call'}]
# [{'name': 'multiply', 'args': {'a': 3}, 'id': 'call_t7mPosFh2RJNjKbITMIJBHDx', 'type': 'tool_call'}]
# [{'name': 'multiply', 'args': {'a': 3, 'b': 1}, 'id': 'call_t7mPosFh2RJNjKbITMIJBHDx', 'type': 'tool_call'}]
# [{'name': 'multiply', 'args': {'a': 3, 'b': 12}, 'id': 'call_t7mPosFh2RJNjKbITMIJBHDx', 'type': 'tool_call'}]
# [{'name': 'multiply', 'args': {'a': 3, 'b': 12}, 'id': 'call_t7mPosFh2RJNjKbITMIJBHDx', 'type': 'tool_call'}, {'name': 'add', 'args': {}, 'id': 'call_ITDqycsucL2YMfMeymxRPJTy', 'type': 'tool_call'}]
# [{'name': 'multiply', 'args': {'a': 3, 'b': 12}, 'id': 'call_t7mPosFh2RJNjKbITMIJBHDx', 'type': 'tool_call'}, {'name': 'add', 'args': {}, 'id': 'call_ITDqycsucL2YMfMeymxRPJTy', 'type': 'tool_call'}]
# [{'name': 'multiply', 'args': {'a': 3, 'b': 12}, 'id': 'call_t7mPosFh2RJNjKbITMIJBHDx', 'type': 'tool_call'}, {'name': 'add', 'args': {'a': 11}, 'id': 'call_ITDqycsucL2YMfMeymxRPJTy', 'type': 'tool_call'}]
# [{'name': 'multiply', 'args': {'a': 3, 'b': 12}, 'id': 'call_t7mPosFh2RJNjKbITMIJBHDx', 'type': 'tool_call'}, {'name': 'add', 'args': {'a': 11}, 'id': 'call_ITDqycsucL2YMfMeymxRPJTy', 'type': 'tool_call'}]
# [{'name': 'multiply', 'args': {'a': 3, 'b': 12}, 'id': 'call_t7mPosFh2RJNjKbITMIJBHDx', 'type': 'tool_call'}, {'name': 'add', 'args': {'a': 11, 'b': 49}, 'id': 'call_ITDqycsucL2YMfMeymxRPJTy', 'type': 'tool_call'}]
# [{'name': 'multiply', 'args': {'a': 3, 'b': 12}, 'id': 'call_t7mPosFh2RJNjKbITMIJBHDx', 'type': 'tool_call'}, {'name': 'add', 'args': {'a': 11, 'b': 49}, 'id': 'call_ITDqycsucL2YMfMeymxRPJTy', 'type': 'tool_call'}]

print(' ')
print(type(gathered.tool_calls[0]["args"]))
# <class 'dict'>