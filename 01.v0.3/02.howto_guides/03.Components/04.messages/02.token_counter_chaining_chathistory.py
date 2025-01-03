# pip install -qU tiktoken

from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
    trim_messages,
)
from langchain_openai import ChatOpenAI

messages = [
    SystemMessage("you're a good assistant, you always respond with a joke."),
    HumanMessage("i wonder why it's called langchain"),
    AIMessage(
        'Well, I guess they thought "WordRope" and "SentenceString" just didn\'t have the same ring to it!'
    ),
    HumanMessage("and who is harrison chasing anyways"),
    AIMessage(
        "Hmmm let me think.\n\nWhy, he's probably chasing after the last cup of coffee in the office!"
    ),
    HumanMessage("what do you call a speechless parrot"),
]


###########################################################
from typing import List

import tiktoken
from langchain_core.messages import BaseMessage, ToolMessage


def str_token_counter(text: str) -> int:
    enc = tiktoken.get_encoding("o200k_base")
    return len(enc.encode(text))


def tiktoken_counter(messages: List[BaseMessage]) -> int:
    """Approximately reproduce https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb

    For simplicity only supports str Message.contents.
    """
    num_tokens = 3  # every reply is primed with <|start|>assistant<|message|>
    tokens_per_message = 3
    tokens_per_name = 1
    for msg in messages:
        if isinstance(msg, HumanMessage):
            role = "user"
        elif isinstance(msg, AIMessage):
            role = "assistant"
        elif isinstance(msg, ToolMessage):
            role = "tool"
        elif isinstance(msg, SystemMessage):
            role = "system"
        else:
            raise ValueError(f"Unsupported messages type {msg.__class__}")
        num_tokens += (
            tokens_per_message
            + str_token_counter(role)
            + str_token_counter(msg.content)
        )
        if msg.name:
            num_tokens += tokens_per_name + str_token_counter(msg.name)
    return num_tokens

#################################################################################
### 1. custom token counter를 사용하여 trim_messages 
print('1.', '-' * 50)
##################################################################################
results = trim_messages(
    messages,
    token_counter=tiktoken_counter,
    # Keep the last <= n_count tokens of the messages.
    strategy="last",
    # When token_counter=len, each message
    # will be counted as a single token.
    # Remember to adjust for your use case
    max_tokens=45,
    # Most chat models expect that chat history starts with either:
    # (1) a HumanMessage or
    # (2) a SystemMessage followed by a HumanMessage
    start_on="human",
    # Most chat models expect that chat history ends with either:
    # (1) a HumanMessage or
    # (2) a ToolMessage
    end_on=("human", "tool"),
    # Usually, we want to keep the SystemMessage
    # if it's present in the original history.
    # The SystemMessage has special instructions for the model.
    include_system=True,
)
rprint(results)
# 1. --------------------------------------------------
# [
#     SystemMessage(content="you're a good assistant, you always respond with a joke.", additional_kwargs={}, response_metadata={}),
#     HumanMessage(content='what do you call a speechless parrot', additional_kwargs={}, response_metadata={})
# ]


#################################################################################
### 2. chaining
print('2.', '-' * 50)
##################################################################################
llm = ChatOpenAI(model="gpt-4o")

# Notice we don't pass in messages. This creates
# a RunnableLambda that takes messages as input
trimmer = trim_messages(
    token_counter=llm,
    # Keep the last <= n_count tokens of the messages.
    strategy="last",
    # When token_counter=len, each message
    # will be counted as a single token.
    # Remember to adjust for your use case
    max_tokens=45,
    # Most chat models expect that chat history starts with either:
    # (1) a HumanMessage or
    # (2) a SystemMessage followed by a HumanMessage
    start_on="human",
    # Most chat models expect that chat history ends with either:
    # (1) a HumanMessage or
    # (2) a ToolMessage
    end_on=("human", "tool"),
    # Usually, we want to keep the SystemMessage
    # if it's present in the original history.
    # The SystemMessage has special instructions for the model.
    include_system=True,
)
### messages없이 trim_messages를 실행하면 RunnableLambda가 생성됩니다.
# rprint(trimmer)
# RunnableLambda(...)

chain = trimmer | llm
rprint(chain.invoke(messages))
# 2. --------------------------------------------------
# AIMessage(
#     content='A polygon!',
#     additional_kwargs={'refusal': None},
#     response_metadata={
#         'token_usage': {
#             'completion_tokens': 4,
#             'prompt_tokens': 32,
#             'total_tokens': 36,
#             'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#             'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
#         },
#         'model_name': 'gpt-4o-2024-08-06',
#         'system_fingerprint': 'fp_d28bcae782',
#         'finish_reason': 'stop',
#         'logprobs': None
#     },
#     id='run-f183809f-353f-4e36-9cd7-81d25172bf48-0',
#     usage_metadata={'input_tokens': 32, 'output_tokens': 4, 'total_tokens': 36, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
# )

print(' ')
rprint(trimmer.invoke(messages))
# [
#     SystemMessage(content="you're a good assistant, you always respond with a joke.", additional_kwargs={}, response_metadata={}),
#     HumanMessage(content='what do you call a speechless parrot', additional_kwargs={}, response_metadata={})
# ]


#################################################################################
### 3.  ChatMessageHistory와 함께 사용
print('3.', '-' * 50)
##################################################################################
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

chat_history = InMemoryChatMessageHistory(messages=messages[:-1])


def dummy_get_session_history(session_id):
    if session_id != "1":
        return InMemoryChatMessageHistory()
    return chat_history


llm = ChatOpenAI(model="gpt-4o")

trimmer = trim_messages(
    max_tokens=45,
    strategy="last",
    token_counter=llm,
    # Usually, we want to keep the SystemMessage
    # if it's present in the original history.
    # The SystemMessage has special instructions for the model.
    include_system=True,
    # Most chat models expect that chat history starts with either:
    # (1) a HumanMessage or
    # (2) a SystemMessage followed by a HumanMessage
    # start_on="human" makes sure we produce a valid chat history
    start_on="human",
)

chain = trimmer | llm
chain_with_history = RunnableWithMessageHistory(chain, dummy_get_session_history)
rprint(chain_with_history.invoke(
    [HumanMessage("what do you call a speechless parrot")],
    config={"configurable": {"session_id": "1"}},
))
# 3. --------------------------------------------------
# AIMessage(
#     content='A polygon!',
#     additional_kwargs={'refusal': None},
#     response_metadata={
#         'token_usage': {
#             'completion_tokens': 4,
#             'prompt_tokens': 32,
#             'total_tokens': 36,
#             'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#             'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
#         },
#         'model_name': 'gpt-4o-2024-08-06',
#         'system_fingerprint': 'fp_d28bcae782',
#         'finish_reason': 'stop',
#         'logprobs': None
#     },
#     id='run-dcaca226-c572-4b30-a89d-aa84459a5ce1-0',
#     usage_metadata={'input_tokens': 32, 'output_tokens': 4, 'total_tokens': 36, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
# )