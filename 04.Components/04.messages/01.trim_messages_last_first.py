from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
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

### 1. last max_tokens - 가장 최근의 메시지부터 시작해서 max_tokens에 도달할 때까지 메시지를 줄임
results = trim_messages(
    messages,
    max_tokens=45,
    strategy="last",
    token_counter=ChatOpenAI(model="gpt-4o"),
)
print(results)
# [AIMessage(content="Hmmm let me think.\n\nWhy, he's probably chasing after the last cup of coffee in the office!"), HumanMessage(content='what do you call a speechless parrot')]


### 2. system massease를 항상 유지하기 - 'include_system=True'
print('-'*30)
results = trim_messages(
    messages,
    max_tokens=45,
    strategy="last",
    token_counter=ChatOpenAI(model="gpt-4o"),
    include_system=True,
)
print(results)
# [SystemMessage(content="you're a good assistant, you always respond with a joke."), HumanMessage(content='what do you call a speechless parrot')]


### 3. 메시지의 내용을 분할 하기 - 'allow_partial=True'
print('-'*30)
results = trim_messages(
    messages,
    max_tokens=56,
    strategy="last",
    token_counter=ChatOpenAI(model="gpt-4o"),
    include_system=True,
    allow_partial=True,
)
print(results)
# [SystemMessage(content="you're a good assistant, you always respond with a joke."), AIMessage(content="\nWhy, he's probably chasing after the last cup of coffee in the office!"), HumanMessage(content='what do you call a speechless parrot')]


### 4. 첫 번째 메시지를 특정 유형이 되도독 설정 - 'start_on' - system messages 제외
print('-'*30)
results = trim_messages(
    messages,
    max_tokens=60,
    strategy="last",
    token_counter=ChatOpenAI(model="gpt-4o"),
    include_system=True,
    start_on="human",
)
print(results)
# [SystemMessage(content="you're a good assistant, you always respond with a joke."), HumanMessage(content='what do you call a speechless parrot')]


### 5. first max_tokens - 'strategy="first"' - 가장 처음의 메시지부터 시작해서 max_tokens에 도달할 때까지 메시지를 줄임
results = trim_messages(
    messages,
    max_tokens=45,
    strategy="first",
    token_counter=ChatOpenAI(model="gpt-4o"),
)
print(results)
# [SystemMessage(content="you're a good assistant, you always respond with a joke."), HumanMessage(content="i wonder why it's called langchain")]