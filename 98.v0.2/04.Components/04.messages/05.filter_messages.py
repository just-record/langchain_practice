from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
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

#### 1. 기본 사용법 - 'include_types="human"'
results = filter_messages(messages, include_types="human")
print(results)
# [HumanMessage(content='example input', name='example_user', id='2'), HumanMessage(content='real input', name='bob', id='4')]


#### 2. 기본 사용법 - 'exclude_names=["example_user", "example_assistant"]'
print('-'*30)
results = filter_messages(messages, exclude_names=["example_user", "example_assistant"])
print(results)
# [SystemMessage(content='you are a good assistant', id='1'), HumanMessage(content='real input', name='bob', id='4'), AIMessage(content='real output', name='alice', id='5')]


#### 3. 기본 사용법 - 'include_types=[HumanMessage, AIMessage], exclude_ids=["3"]'
print('-'*30)
results = filter_messages(messages, include_types=[HumanMessage, AIMessage], exclude_ids=["3"])
print(results)
# [HumanMessage(content='example input', name='example_user', id='2'), HumanMessage(content='real input', name='bob', id='4'), AIMessage(content='real output', name='alice', id='5')]


### 4. Chaining
print('-'*30)
# Notice we don't pass in messages. This creates a RunnableLambda that takes messages as input
llm = ChatOpenAI(model="gpt-4o")
filter_ = filter_messages(exclude_names=["example_user", "example_assistant"])
chain = filter_ | llm
results = chain.invoke(messages)
print(results)
