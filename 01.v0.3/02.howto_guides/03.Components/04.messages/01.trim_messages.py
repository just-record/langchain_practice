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


#################################################################################
### 1. Token 개수를 기준으로 하는 trim_messages
print('1.', '-' * 50)
##################################################################################
results = trim_messages(
    messages,
    # Keep the last <= n_count tokens of the messages.
    strategy="last",
    # Remember to adjust based on your model
    # or else pass a custom token_encoder
    token_counter=ChatOpenAI(model="gpt-4o"),
    # Most chat models expect that chat history starts with either:
    # (1) a HumanMessage or
    # (2) a SystemMessage followed by a HumanMessage
    # Remember to adjust based on the desired conversation
    # length
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
    allow_partial=False,
)
rprint(results)
# 1. --------------------------------------------------
# [
#     SystemMessage(content="you're a good assistant, you always respond with a joke.", additional_kwargs={}, response_metadata={}),
#     HumanMessage(content='what do you call a speechless parrot', additional_kwargs={}, response_metadata={})
# ]


#################################################################################
### 2. message 개수를 기준으로 하는 trim_messages
### token_counter=ChatOpenAI(model="gpt-4o") 없음
print('2.', '-' * 50)
##################################################################################
results = trim_messages(
    messages,
    # Keep the last <= n_count tokens of the messages.
    strategy="last",
    token_counter=len,
    # When token_counter=len, each message
    # will be counted as a single token.
    # Remember to adjust for your use case
    max_tokens=5,
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
# 2. --------------------------------------------------
# [
#     SystemMessage(content="you're a good assistant, you always respond with a joke.", additional_kwargs={}, response_metadata={}),
#     HumanMessage(content='and who is harrison chasing anyways', additional_kwargs={}, response_metadata={}),
#     AIMessage(content="Hmmm let me think.\n\nWhy, he's probably chasing after the last cup of coffee in the office!", additional_kwargs={}, response_metadata={}),
#     HumanMessage(content='what do you call a speechless parrot', additional_kwargs={}, response_metadata={})
# ]


#################################################################################
### 3. Advanced Usage 
### allow_partial=True => message 내용을 분할 가능
print('3.', '-' * 50)
##################################################################################
results = trim_messages(
    messages,
    max_tokens=56,
    strategy="last",
    token_counter=ChatOpenAI(model="gpt-4o"),
    include_system=True,
    allow_partial=True,
)
rprint(results)
# 3. --------------------------------------------------
# [
#     SystemMessage(content="you're a good assistant, you always respond with a joke.", additional_kwargs={}, response_metadata={}),
#     AIMessage(content="\nWhy, he's probably chasing after the last cup of coffee in the office!", additional_kwargs={}, response_metadata={}),
#     HumanMessage(content='what do you call a speechless parrot', additional_kwargs={}, response_metadata={})
# ]


#################################################################################
### 4. Advanced Usage 
### include_system=False 또는 include_system argument 생략하면 SystemMessage를 제외
print('4.', '-' * 50)
##################################################################################
results = trim_messages(
    messages,
    max_tokens=45,
    strategy="last",
    token_counter=ChatOpenAI(model="gpt-4o"),
)
rprint(results)
# 4. --------------------------------------------------
# [
#     AIMessage(content="Hmmm let me think.\n\nWhy, he's probably chasing after the last cup of coffee in the office!", additional_kwargs={}, response_metadata={}),
#     HumanMessage(content='what do you call a speechless parrot', additional_kwargs={}, response_metadata={})
# ]


#################################################################################
### 5. Advanced Usage 
### strategy="first"로 처음부터 max_tokens까지의 message를 반환
print('5.', '-' * 50)
##################################################################################
results = trim_messages(
    messages,
    max_tokens=45,
    strategy="first",
    token_counter=ChatOpenAI(model="gpt-4o"),
)
rprint(results)
# 5. --------------------------------------------------
# [
#     SystemMessage(content="you're a good assistant, you always respond with a joke.", additional_kwargs={}, response_metadata={}),
#     HumanMessage(content="i wonder why it's called langchain", additional_kwargs={}, response_metadata={})
# ]