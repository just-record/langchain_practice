#################################
### 사용자 Tool 정의 하기 ###
# 1. 또는 2. 선택: 1. 사용 시에는 2. 주석 처리 - 2. 사용 시에는 1. 주석 처리
#################################

#################################
### 1. @tool decorator 사용하기
# from langchain_core.tools import tool


# @tool
# def add(a: int, b: int) -> int:
#     """Adds a and b."""
#     print(f'called add() => a: {a}, b: {b}')
#     return a + b


# @tool
# def multiply(a: int, b: int) -> int:
#     """Multiplies a and b."""
#     print(f'called multiply() => a: {a}, b: {b}')
#     return a * b


# tools = [add, multiply]
#################################


#################################
### 2. Pydantic을 사용하여 Tool 정의하기
from langchain_core.pydantic_v1 import BaseModel, Field


# Note that the docstrings here are crucial, as they will be passed along
# to the model along with the class name.
class Add(BaseModel):
    """Add two integers together."""

    a: int = Field(..., description="First integer")
    b: int = Field(..., description="Second integer")


class Multiply(BaseModel):
    """Multiply two integers together."""

    a: int = Field(..., description="First integer")
    b: int = Field(..., description="Second integer")


tools = [Add, Multiply]
#################################



from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo")

### chat models에 binding 하기
llm_with_tools = llm.bind_tools(tools)

query = "What is 3 * 12?"

results = llm_with_tools.invoke(query)
print(results)
# content='' additional_kwargs={'tool_calls': [{'id': 'call_NrWdLoJ8pZjTbx4Tq1cX78DU', 'function': {'arguments': '{"a": 3, "b": 12}', 'name': 'multiply'}, 'type': 'function'}]} response_metadata={'token_usage': {'completion_tokens': 32, 'prompt_tokens': 78, 'total_tokens': 110}, 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'finish_reason': 'tool_calls', 'logprobs': None} id='run-b5ea265d-3cab-4627-a8a1-1c633eec36c2-0' tool_calls=[{'name': 'multiply', 'args': {'a': 3, 'b': 12}, 'id': 'call_NrWdLoJ8pZjTbx4Tq1cX78DU'}] usage_metadata={'input_tokens': 78, 'output_tokens': 32, 'total_tokens': 110}
### 함수를 호출 한 건 아님 => 함수와 인자 정보를 생성 => tool_calls=[{'name': 'multiply', 'args': {'a': 3, 'b': 12}, 'id': 'call_Ku3VMDq8zhZcba6uDGuz5cGD'}]

### Tool calls ###
print('-'*30)
query = "What is 3 * 12? Also, what is 11 + 49?"

print(llm_with_tools.invoke(query).tool_calls)
# [{'name': 'multiply', 'args': {'a': 3, 'b': 12}, 'id': 'call_FrWIUdoyvOWg7qnbSd4QLWpS'}, {'name': 'add', 'args': {'a': 11, 'b': 49}, 'id': 'call_yc3UZNcET8VQvqSBCqWSIvEH'}]


### 'PydanticToolsParser'를 사용 하여 원래 Pydantic 클래스로 결과를 파싱
# '2. Pydantic을 사용하여 Tool 정의하기'를 사용
print('-'*30)
from langchain_core.output_parsers import PydanticToolsParser

chain = llm_with_tools | PydanticToolsParser(tools=[Multiply, Add])
results = chain.invoke(query)
print(results)
# [Multiply(a=3, b=12), Add(a=11, b=49)]