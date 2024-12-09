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

llm = ChatOpenAI(model="gpt-4o")

### 1. chain으로 trimmer와 llm을 연결하기
# Notice we don't pass in messages. This creates a RunnableLambda that takes messages as input
trimmer = trim_messages(
    max_tokens=45,
    strategy="last",
    token_counter=llm,
    include_system=True,
)

chain = trimmer | llm
results = chain.invoke(messages)
print(results)
# content='A polygon! Because it\'s a "poly-gone"! 😄' response_metadata={'token_usage': {'completion_tokens': 13, 'prompt_tokens': 32, 'total_tokens': 45}, 'model_name': 'gpt-4o-2024-05-13', 'system_fingerprint': 'fp_d576307f90', 'finish_reason': 'stop', 'logprobs': None} id='run-1b9b00f2-6866-4255-99d3-4d9af8a8b4dd-0' usage_metadata={'input_tokens': 32, 'output_tokens': 13, 'total_tokens': 45}


### 2. trimmer 만 보기
print('-'*30)
results = trimmer.invoke(messages)
print(results)
# [SystemMessage(content="you're a good assistant, you always respond with a joke."), HumanMessage(content='what do you call a speechless parrot')]