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
### 1. 모델이 특정 도구를 호출하도록 강제하기
### tool_choice=
print('1.', '-' * 50)
################################################################################## 
llm_forced_to_multiply = llm.bind_tools(tools, tool_choice="multiply")
rprint(llm_forced_to_multiply.invoke("what is 2 + 4"))
# 1. --------------------------------------------------
# AIMessage(
#     content='',
#     additional_kwargs={'tool_calls': [{'id': 'call_dxrUvVvyuns24HJqN3zSlnTL', 'function': {'arguments': '{"a":2,"b":4}', 'name': 'multiply'}, 'type': 'function'}], 'refusal': None},
#     response_metadata={
#         'token_usage': {
#             'completion_tokens': 10,
#             'prompt_tokens': 84,
#             'total_tokens': 94,
#             'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#             'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
#         },
#         'model_name': 'gpt-4o-mini-2024-07-18',
#         'system_fingerprint': 'fp_0aa8d3e20b',
#         'finish_reason': 'stop',
#         'logprobs': None
#     },
#     id='run-3d35a0f6-d1f4-4682-a0f5-272104e563c3-0',
#     tool_calls=[{'name': 'multiply', 'args': {'a': 2, 'b': 4}, 'id': 'call_dxrUvVvyuns24HJqN3zSlnTL', 'type': 'tool_call'}],
#     usage_metadata={'input_tokens': 84, 'output_tokens': 10, 'total_tokens': 94, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
# )


#################################################################################
### 2. 도구 중에 하나를 선택하도록 강제하기
### tool_choice="any"
print('2.', '-' * 50)
################################################################################## 
llm_forced_to_use_tool = llm.bind_tools(tools, tool_choice="any")
rprint(llm_forced_to_use_tool.invoke("What day is today?"))
# 2. --------------------------------------------------
# AIMessage(
#     content='',
#     additional_kwargs={'tool_calls': [{'id': 'call_PtWwR1JsvKYxh4ENwEv0v5iK', 'function': {'arguments': '{"a":0,"b":0}', 'name': 'add'}, 'type': 'function'}], 'refusal': None},
#     response_metadata={
#         'token_usage': {
#             'completion_tokens': 18,
#             'prompt_tokens': 74,
#             'total_tokens': 92,
#             'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#             'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
#         },
#         'model_name': 'gpt-4o-mini-2024-07-18',
#         'system_fingerprint': 'fp_0aa8d3e20b',
#         'finish_reason': 'tool_calls',
#         'logprobs': None
#     },
#     id='run-4ce86983-b0a4-4adc-a981-8427007bc790-0',
#     tool_calls=[{'name': 'add', 'args': {'a': 0, 'b': 0}, 'id': 'call_PtWwR1JsvKYxh4ENwEv0v5iK', 'type': 'tool_call'}],
#     usage_metadata={'input_tokens': 74, 'output_tokens': 18, 'total_tokens': 92, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
# )