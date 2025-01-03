from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    filter_messages,
)

messages = [
    SystemMessage("you are a good assistant", id="1"),
    HumanMessage("example input", id="2", name="example_user"),
    AIMessage("example output", id="3", name="example_assistant"),
    HumanMessage("real input", id="4", name="bob"),
    AIMessage("real output", id="5", name="alice"),
]


#################################################################################
### 1. filter_messages: include_types="human"
print('1.', '-' * 50)
##################################################################################
rprint(filter_messages(messages, include_types="human"))
# 1. --------------------------------------------------
# [HumanMessage(content='example input', additional_kwargs={}, response_metadata={}, name='example_user', id='2'), HumanMessage(content='real input', additional_kwargs={}, response_metadata={}, name='bob', id='4')]


#################################################################################
### 2. filter_messages: exclude_names
print('2.', '-' * 50)
##################################################################################
rprint(filter_messages(messages, exclude_names=["example_user", "example_assistant"]))
# 2. --------------------------------------------------
# [
#     SystemMessage(content='you are a good assistant', additional_kwargs={}, response_metadata={}, id='1'),
#     HumanMessage(content='real input', additional_kwargs={}, response_metadata={}, name='bob', id='4'),
#     AIMessage(content='real output', additional_kwargs={}, response_metadata={}, name='alice', id='5')
# ]


#################################################################################
### 3. filter_messages: include_types and exclude_ids
print('3.', '-' * 50)
##################################################################################
rprint(filter_messages(messages, include_types=[HumanMessage, AIMessage], exclude_ids=["3"]))
# 3. --------------------------------------------------
# [
#     HumanMessage(content='example input', additional_kwargs={}, response_metadata={}, name='example_user', id='2'),
#     HumanMessage(content='real input', additional_kwargs={}, response_metadata={}, name='bob', id='4'),
#     AIMessage(content='real output', additional_kwargs={}, response_metadata={}, name='alice', id='5')
# ]


#################################################################################
### 4. chaining
### filter_messages에서 messages 제외 -> RunnableLambda(...)
print('4.', '-' * 50)
##################################################################################
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o", temperature=0)
# Notice we don't pass in messages. This creates
# a RunnableLambda that takes messages as input
filter_ = filter_messages(exclude_names=["example_user", "example_assistant"])
# rprint(filter_)
# RunnableLambda(...)
chain = filter_ | llm
rprint(chain.invoke(messages))
# 4. --------------------------------------------------
# AIMessage(
#     content='How can I assist you today?',
#     additional_kwargs={'refusal': None},
#     response_metadata={
#         'token_usage': {
#             'completion_tokens': 8,
#             'prompt_tokens': 28,
#             'total_tokens': 36,
#             'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#             'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
#         },
#         'model_name': 'gpt-4o-2024-08-06',
#         'system_fingerprint': 'fp_5f20662549',
#         'finish_reason': 'stop',
#         'logprobs': None
#     },
#     id='run-5f8e03c5-a231-45b6-9a4a-974b2563ea89-0',
#     usage_metadata={'input_tokens': 28, 'output_tokens': 8, 'total_tokens': 36, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
# )

print(' ') 
rprint(filter_.invoke(messages))
# [
#     SystemMessage(content='you are a good assistant', additional_kwargs={}, response_metadata={}, id='1'),
#     HumanMessage(content='real input', additional_kwargs={}, response_metadata={}, name='bob', id='4'),
#     AIMessage(content='real output', additional_kwargs={}, response_metadata={}, name='alice', id='5')
# ]