from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool


llm = ChatOpenAI(model="gpt-4o-mini")


@tool
def add(a: int, b: int) -> int:
    """Adds a and b."""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiplies a and b."""
    return a * b


tools = [add, multiply]

llm_with_tools = llm.bind_tools(tools)


#################################################################################
### 1. tool이 bind된 모델의 invoke 결과 확인
### 결과 값을 messages list에 append 하여 conversation history 관리
print('1.', '-' * 50)
################################################################################## 
from langchain_core.messages import HumanMessage

query = "What is 3 * 12? Also, what is 11 + 49?"
messages = [HumanMessage(query)]
ai_msg = llm_with_tools.invoke(messages)
rprint(ai_msg.tool_calls)
# 1. --------------------------------------------------
# [
#     {'name': 'multiply', 'args': {'a': 3, 'b': 12}, 'id': 'call_mv6gJDYtQ0PoflZTZpQDZa8a', 'type': 'tool_call'},
#     {'name': 'add', 'args': {'a': 11, 'b': 49}, 'id': 'call_V4Cnckd4Ax2yqHUX4ZQ9TWAV', 'type': 'tool_call'}
# ]
messages.append(ai_msg)


#################################################################################
### 2. 모델이 생성한 args를 사용 하여 tool function을 invoke
### LangChain Tool을 ToolCall과 함께 호출하면 모델에 다시 전달할 수 있는 ToolMessage가 자동으로 반환
print('2.', '-' * 50)
################################################################################## 
for tool_call in ai_msg.tool_calls:
    selected_tool = {"add": add, "multiply": multiply}[tool_call["name"].lower()]
    tool_msg = selected_tool.invoke(tool_call)
    messages.append(tool_msg)

rprint(messages)
# 2. --------------------------------------------------
# [
#     HumanMessage(content='What is 3 * 12? Also, what is 11 + 49?', additional_kwargs={}, response_metadata={}),
#     AIMessage(
#         content='',
#         additional_kwargs={
#             'tool_calls': [
#                 {'id': 'call_lMTkrAaxc1cDCS9ea8GIWcJu', 'function': {'arguments': '{"a": 3, "b": 12}', 'name': 'multiply'}, 'type': 'function'},
#                 {'id': 'call_njRRm5KXtKjBvRk19XWY0ZpY', 'function': {'arguments': '{"a": 11, "b": 49}', 'name': 'add'}, 'type': 'function'}
#             ],
#             'refusal': None
#         },
#         response_metadata={
#             'token_usage': {
#                 'completion_tokens': 51,
#                 'prompt_tokens': 87,
#                 'total_tokens': 138,
#                 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#                 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
#             },
#             'model_name': 'gpt-4o-mini-2024-07-18',
#             'system_fingerprint': 'fp_0aa8d3e20b',
#             'finish_reason': 'tool_calls',
#             'logprobs': None
#         },
#         id='run-7096d2e6-d9dd-430c-9e92-42a4cfdb30d9-0',
#         tool_calls=[
#             {'name': 'multiply', 'args': {'a': 3, 'b': 12}, 'id': 'call_lMTkrAaxc1cDCS9ea8GIWcJu', 'type': 'tool_call'},
#             {'name': 'add', 'args': {'a': 11, 'b': 49}, 'id': 'call_njRRm5KXtKjBvRk19XWY0ZpY', 'type': 'tool_call'}
#         ],
#         usage_metadata={'input_tokens': 87, 'output_tokens': 51, 'total_tokens': 138, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
#     ),
#     ToolMessage(content='36', name='multiply', tool_call_id='call_lMTkrAaxc1cDCS9ea8GIWcJu'),
#     ToolMessage(content='60', name='add', tool_call_id='call_njRRm5KXtKjBvRk19XWY0ZpY')
# ]


#################################################################################
### 3. tool function이 반환한 결과를 가지고 모델 invoke
### 원래 요청에 의한 최종 답변 생성
print('3.', '-' * 50)
################################################################################## 
rprint(llm_with_tools.invoke(messages))
# 3. --------------------------------------------------
# AIMessage(
#     content='The result of 3 * 12 is 36, and the result of 11 + 49 is 60.',
#     additional_kwargs={'refusal': None},
#     response_metadata={
#         'token_usage': {
#             'completion_tokens': 27,
#             'prompt_tokens': 153,
#             'total_tokens': 180,
#             'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#             'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
#         },
#         'model_name': 'gpt-4o-mini-2024-07-18',
#         'system_fingerprint': 'fp_0aa8d3e20b',
#         'finish_reason': 'stop',
#         'logprobs': None
#     },
#     id='run-ea5adacd-ae95-4765-9f8b-6f549da327ff-0',
#     usage_metadata={'input_tokens': 153, 'output_tokens': 27, 'total_tokens': 180, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
# )