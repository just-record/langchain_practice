from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableParallel


def get_session_history(session_id):
    return SQLChatMessageHistory(session_id, connection="sqlite:///memory.db")

model = ChatOpenAI(model="gpt-3.5-turbo")

chain = RunnableParallel({"output_message": model})

runnable_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    output_messages_key="output_message",
)

### 1. 첫번째 질의: 난 bob이야!, session_id: 1
results = runnable_with_history.invoke(
    [HumanMessage(content="hi - im bob!")],
    config={"configurable": {"session_id": "3"}},
)
print(results)
# 출력
# {'output_message': AIMessage(content='Hello Bob! Nice to meet you. How can I assist you today?', response_metadata={'token_usage': {'completion_tokens': 15, 'prompt_tokens': 12, 'total_tokens': 27}, 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None}, id='run-787374a2-e8c1-48b3-bdf7-6f580a695015-0', usage_metadata={'input_tokens': 12, 'output_tokens': 15, 'total_tokens': 27})}
print('-'*30)

### 2. 두번째 질의: 내 이름이 뭐야?, session_id: 1 - 첫번째 질의의 이름을 기억
results = runnable_with_history.invoke(
    [HumanMessage(content="whats my name?")],
    config={"configurable": {"session_id": "3"}},
)
print(results)
# 출력
# {'output_message': AIMessage(content='Your name is Bob!', response_metadata={'token_usage': {'completion_tokens': 5, 'prompt_tokens': 40, 'total_tokens': 45}, 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None}, id='run-98d3cd61-3195-4837-aa14-e571edd140f8-0', usage_metadata={'input_tokens': 40, 'output_tokens': 5, 'total_tokens': 45})}
print('-'*30)

### 3. 세번째 질의: 내 이름이 뭐야?, session_id: 2a(다른 session_id) - 첫번 째 질의의  이름을 기억하지 못함
results = runnable_with_history.invoke(
    [HumanMessage(content="whats my name?")],
    config={"configurable": {"session_id": "3a"}},
)
print(results)
# 출력
# {'output_message': AIMessage(content="I'm sorry, I do not know your name as I am an AI assistant and do not have access to personal information.", response_metadata={'token_usage': {'completion_tokens': 25, 'prompt_tokens': 12, 'total_tokens': 37}, 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None}, id='run-df77831c-3de7-44a6-ac8b-0f955c56ba1d-0', usage_metadata={'input_tokens': 12, 'output_tokens': 25, 'total_tokens': 37})}

