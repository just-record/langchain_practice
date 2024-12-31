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

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

#################################################################################
### 1. 특정 tool을 강제로 호출 하기
### tool_choice="multiply"
print('1.', '-' * 50)
##################################################################################
llm_forced_to_multiply = llm.bind_tools(tools, tool_choice="multiply")
rprint(llm_forced_to_multiply.invoke("what is 2 + 4"))
# 1. --------------------------------------------------
# AIMessage(
#     content='',
#     additional_kwargs={'tool_calls': [{'id': 'call_bh9yN3xh8ofk5ExJk8aI9Jsb', 'function': {'arguments': '{"a":2,"b":4}', 'name': 'multiply'}, 'type': 'function'}], 'refusal': None},
#     response_metadata={
#         'token_usage': {
#             'completion_tokens': 10,
#             'prompt_tokens': 84,
#             'total_tokens': 94,
#             'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#             'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
#         },
#         'model_name': 'gpt-4o-mini-2024-07-18',
#         'system_fingerprint': 'fp_d02d531b47',
#         'finish_reason': 'stop',
#         'logprobs': None
#     },
#     id='run-596f66b5-074b-41ea-a910-60697409d02b-0',
#     tool_calls=[{'name': 'multiply', 'args': {'a': 2, 'b': 4}, 'id': 'call_bh9yN3xh8ofk5ExJk8aI9Jsb', 'type': 'tool_call'}],
#     usage_metadata={'input_tokens': 84, 'output_tokens': 10, 'total_tokens': 94, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
# )


#################################################################################
### 2. 바인딩 된 tool 중 하나를 강제로 호출 하기
### tool_choice="any"
print('2.', '-' * 50)
##################################################################################
llm_forced_to_use_tool = llm.bind_tools(tools, tool_choice="any")
rprint(llm_forced_to_use_tool.invoke("What day is today?"))
# 2. --------------------------------------------------
# AIMessage(
#     content='',
#     additional_kwargs={'tool_calls': [{'id': 'call_tUf6ErbAlC3gJttCR2VlctMP', 'function': {'arguments': '{"a":1,"b":1}', 'name': 'add'}, 'type': 'function'}], 'refusal': None},
#     response_metadata={
#         'token_usage': {
#             'completion_tokens': 18,
#             'prompt_tokens': 74,
#             'total_tokens': 92,
#             'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#             'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
#         },
#         'model_name': 'gpt-4o-mini-2024-07-18',
#         'system_fingerprint': 'fp_d02d531b47',
#         'finish_reason': 'tool_calls',
#         'logprobs': None
#     },
#     id='run-daf8cfb3-ac5d-43e4-93df-52a9bde2a1fe-0',
#     tool_calls=[{'name': 'add', 'args': {'a': 1, 'b': 1}, 'id': 'call_tUf6ErbAlC3gJttCR2VlctMP', 'type': 'tool_call'}],
#     usage_metadata={'input_tokens': 74, 'output_tokens': 18, 'total_tokens': 92, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
# )
