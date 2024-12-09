from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    merge_message_runs,
)

messages = [
    SystemMessage("you're a good assistant."),
    SystemMessage("you always respond with a joke."),
    HumanMessage([{"type": "text", "text": "i wonder why it's called langchain"}]),
    HumanMessage("and who is harrison chasing anyways"),
    AIMessage(
        'Well, I guess they thought "WordRope" and "SentenceString" just didn\'t have the same ring to it!'
    ),
    AIMessage("Why, he's probably chasing after the last cup of coffee in the office!"),
]

### 1. 기본 사용법 - 'merge_message_runs(messages)'
merged = merge_message_runs(messages)
print("\n\n".join([repr(x) for x in merged]))
# SystemMessage(content="you're a good assistant.\nyou always respond with a joke.")
# 
# HumanMessage(content=[{'type': 'text', 'text': "i wonder why it's called langchain"}, 'and who is harrison chasing anyways'])
# 
# AIMessage(content='Well, I guess they thought "WordRope" and "SentenceString" just didn\'t have the same ring to it!\nWhy, he\'s probably chasing after the last cup of coffee in the office!')


### 2. Chaining
print('-'*30)
## OpenAI로 하면 에러 발생
# llm = ChatOpenAI(model="gpt-4o", temperature=0)
# merger = merge_message_runs()
# chain = merger | llm
# results = chain.invoke(messages)
# print(results)

## Anthropic - claude는 잘 됨
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0)
# Notice we don't pass in messages. This creates a RunnableLambda that takes messages as input
merger = merge_message_runs()
chain = merger | llm
results = chain.invoke(messages)
print(results)
# content=[] response_metadata={'id': 'msg_01URd5QSoHkNBn8E2XjzpHoy', 'model': 'claude-3-sonnet-20240229', 'stop_reason': 'end_turn', 'stop_sequence': None, 'usage': {'input_tokens': 84, 'output_tokens': 3}} id='run-be48e70b-a4b5-4758-8c3d-4febe7c4fb0e-0' usage_metadata={'input_tokens': 84, 'output_tokens': 3, 'total_tokens': 87}

### 3. merger만 확인
print('-'*30)
results = merger.invoke(messages)
print(results)
# [SystemMessage(content="you're a good assistant.\nyou always respond with a joke."), HumanMessage(content=[{'type': 'text', 'text': "i wonder why it's called langchain"}, 'and who is harrison chasing anyways']), AIMessage(content='Well, I guess they thought "WordRope" and "SentenceString" just didn\'t have the same ring to it!\nWhy, he\'s probably chasing after the last cup of coffee in the office!')]