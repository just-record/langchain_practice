from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage


@tool
def add(a: int, b: int) -> int:
    """Adds a and b."""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiplies a and b."""
    return a * b


tools = [add, multiply]

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
llm_with_tools = llm.bind_tools(tools)

query = "What is 3 * 12? Also, what is 11 + 49?"

messages = [HumanMessage(query)]
### 1. query에 대한 Chat model의 응답 받기 - tool_calls의 정보를 return 받음
ai_msg = llm_with_tools.invoke(messages)
### 2. tool_calls에 대한 결과 대화 이력에 추가하기
messages.append(ai_msg)

### 3. tool_calls에 결과에 해당하는 실제 함수를 호출하기 -> 함수 호출 결과를 대화 이력에 추가하기(함수를 여러 개 일 수 있음) 
for tool_call in ai_msg.tool_calls:
    selected_tool = {"add": add, "multiply": multiply}[tool_call["name"].lower()]
    tool_output = selected_tool.invoke(tool_call["args"])
    messages.append(ToolMessage(tool_output, tool_call_id=tool_call["id"]))

for message in messages:
    print(message)
    print('-'*30)
# content='What is 3 * 12? Also, what is 11 + 49?'
# ------------------------------
# content='' additional_kwargs={'tool_calls': [{'id': 'call_ljSh6jIm7V0pFsBWh4kkA8cS', 'function': {'arguments': '{"a": 3, "b": 12}', 'name': 'multiply'}, 'type': 'function'}, {'id': 'call_BE8LjuLPYBjqdH3hTdcaHrt5', 'function': {'arguments': '{"a": 11, "b": 49}', 'name': 'add'}, 'type': 'function'}]} response_metadata={'token_usage': {'completion_tokens': 49, 'prompt_tokens': 88, 'total_tokens': 137}, 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'finish_reason': 'tool_calls', 'logprobs': None} id='run-58087ca9-97f9-4265-a9e6-6f55ef42ce0b-0' tool_calls=[{'name': 'multiply', 'args': {'a': 3, 'b': 12}, 'id': 'call_ljSh6jIm7V0pFsBWh4kkA8cS'}, {'name': 'add', 'args': {'a': 11, 'b': 49}, 'id': 'call_BE8LjuLPYBjqdH3hTdcaHrt5'}] usage_metadata={'input_tokens': 88, 'output_tokens': 49, 'total_tokens': 137}
# ------------------------------
# content='36' tool_call_id='call_ljSh6jIm7V0pFsBWh4kkA8cS'
# ------------------------------
# content='60' tool_call_id='call_BE8LjuLPYBjqdH3hTdcaHrt5'
# ------------------------------

### 모델에서 받은 동일한 id를 Tool message에 전달한다. ###
# 'call_ljSh6jIm7V0pFsBWh4kkA8cS'
# 'call_BE8LjuLPYBjqdH3hTdcaHrt5'


### 4. 함수를 호출 한 결과까지 이력에 포함에 대화를 Chat model에 요청 하기
print('-'*30)
print(llm_with_tools.invoke(messages))
# content='3 * 12 is 36 and 11 + 49 is 60.' response_metadata={'token_usage': {'completion_tokens': 18, 'prompt_tokens': 153, 'total_tokens': 171}, 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None} id='run-a8032553-7a67-428a-b0c2-b7d0be40691a-0' usage_metadata={'input_tokens': 153, 'output_tokens': 18, 'total_tokens': 171}