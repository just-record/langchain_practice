from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableParallel
from operator import itemgetter


def get_session_history(session_id):
    return SQLChatMessageHistory(session_id, connection="sqlite:///memory.db")

model = ChatOpenAI(model="gpt-3.5-turbo")

# chain = RunnableParallel({"output_message": model})

runnable_with_history = RunnableWithMessageHistory(
    itemgetter("input_messages") | model,
    get_session_history,
    input_messages_key="input_messages",
)

### 1. 첫번째 질의: 난 bob이야!, session_id: 1
results = runnable_with_history.invoke(
    {"input_messages": [HumanMessage(content="hi - im bob!")]},
    config={"configurable": {"session_id": "4"}},
)
print(results)
# 출력
# content='Hello Bob! How can I assist you today?' response_metadata={'token_usage': {'completion_tokens': 10, 'prompt_tokens': 12, 'total_tokens': 22}, 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None} id='run-8d74326f-59e0-4cc9-9b92-eab463f67981-0' usage_metadata={'input_tokens': 12, 'output_tokens': 10, 'total_tokens': 22}
print('-'*30)

### 2. 두번째 질의: 내 이름이 뭐야?, session_id: 1 - 첫번째 질의의 이름을 기억
results = runnable_with_history.invoke(
    {"input_messages": [HumanMessage(content="whats my name?")]},
    config={"configurable": {"session_id": "4"}},
)
print(results)
# 출력
# content='Your name is Bob!' response_metadata={'token_usage': {'completion_tokens': 5, 'prompt_tokens': 35, 'total_tokens': 40}, 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None} id='run-9de52e72-1d05-4c1f-b2f7-b1a045abf839-0' usage_metadata={'input_tokens': 35, 'output_tokens': 5, 'total_tokens': 40}
print('-'*30)

### 3. 세번째 질의: 내 이름이 뭐야?, session_id: 2a(다른 session_id) - 첫번 째 질의의  이름을 기억하지 못함
results = runnable_with_history.invoke(
    {"input_messages": [HumanMessage(content="whats my name?")]},
    config={"configurable": {"session_id": "4a"}},
)
print(results)
# 출력
# content="I'm sorry, I do not know your name as I am an AI assistant and do not have that information." response_metadata={'token_usage': {'completion_tokens': 23, 'prompt_tokens': 12, 'total_tokens': 35}, 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None} id='run-4151fe69-0cf0-43b3-9355-5ed2e7cc7853-0' usage_metadata={'input_tokens': 12, 'output_tokens': 23, 'total_tokens': 35}

