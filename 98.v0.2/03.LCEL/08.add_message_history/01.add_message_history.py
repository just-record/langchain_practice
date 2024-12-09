from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.messages import HumanMessage
from langchain_core.runnables.history import RunnableWithMessageHistory


def get_session_history(session_id):
    # 공식 예제 코드: return SQLChatMessageHistory(session_id, "sqlite:///memory.db")
    return SQLChatMessageHistory(session_id, connection="sqlite:///memory.db")

model = ChatOpenAI(model="gpt-3.5-turbo")

runnable_with_history = RunnableWithMessageHistory(
    model,
    get_session_history,
)

### 1. 첫번째 질의: 난 bob이야!, session_id: 1
results = runnable_with_history.invoke(
    HumanMessage(content="hi - im bob!"),
    config={"configurable": {"session_id": "1"}},
)
print(results)
# 출력
# content='Hello Bob! Nice to meet you. How can I assist you today?' response_metadata={'token_usage': {'completion_tokens': 15, 'prompt_tokens': 196, 'total_tokens': 211}, 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None} id='run-cd46febf-8304-411a-9c7e-ba40f1d3e479-0' usage_metadata={'input_tokens': 196, 'output_tokens': 15, 'total_tokens': 211}
print('-'*30)

### 2. 두번째 질의: 내 이름이 뭐야?, session_id: 1 - 첫번째 질의의 이름을 기억
results = runnable_with_history.invoke(
    HumanMessage(content="whats my name?"),
    config={"configurable": {"session_id": "1"}},
)
print(results)
# 출력
# content='Your name is Bob!' response_metadata={'token_usage': {'completion_tokens': 5, 'prompt_tokens': 224, 'total_tokens': 229}, 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None} id='run-ca9406c3-0c94-4254-bbb1-ab640272dce3-0' usage_metadata={'input_tokens': 224, 'output_tokens': 5, 'total_tokens': 229}
print('-'*30)

### 3. 세번째 질의: 내 이름이 뭐야?, session_id: 1a(다른 session_id) - 첫번 째 질의의  이름을 기억하지 못함
results = runnable_with_history.invoke(
    HumanMessage(content="whats my name?"),
    config={"configurable": {"session_id": "1a"}},
)
print(results)
# 출력
# content="I'm sorry, but I cannot determine your name." response_metadata={'token_usage': {'completion_tokens': 11, 'prompt_tokens': 131, 'total_tokens': 142}, 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None} id='run-366f1d18-6433-4dac-9ddb-6097d0a8e9a2-0' usage_metadata={'input_tokens': 131, 'output_tokens': 11, 'total_tokens': 142}