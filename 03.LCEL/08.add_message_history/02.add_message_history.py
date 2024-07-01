from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.messages import HumanMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


def get_session_history(session_id):
    return SQLChatMessageHistory(session_id, connection="sqlite:///memory.db")


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You're an assistant who speaks in {language}. Respond in 20 words or fewer",
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)

model = ChatOpenAI(model="gpt-3.5-turbo")

runnable = prompt | model

runnable_with_history = RunnableWithMessageHistory(
    runnable,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

### 1. 첫번째 질의: 난 bob이야!, session_id: 1
results = runnable_with_history.invoke(
    {"language": "Korean", "input": "hi im bob!"},
    config={"configurable": {"session_id": "2"}},
)
print(results)
# 출력
# content='안녕하세요, 밥님! 무엇을 도와드릴까요?' response_metadata={'token_usage': {'completion_tokens': 26, 'prompt_tokens': 55, 'total_tokens': 81}, 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None} id='run-f8410fbe-20ee-46d6-ae5c-c8ab00683e82-0' usage_metadata={'input_tokens': 55, 'output_tokens': 26, 'total_tokens': 81}
print('-'*30)

### 2. 두번째 질의: 내 이름이 뭐야?, session_id: 1 - 첫번째 질의의 이름을 기억
results = runnable_with_history.invoke(
    {"language": "Korean", "input": "whats my name?"},
    config={"configurable": {"session_id": "2"}},
)
print(results)
# 출력
# content='당신의 이름은 밥입니다!' response_metadata={'token_usage': {'completion_tokens': 9, 'prompt_tokens': 94, 'total_tokens': 103}, 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None} id='run-745d5236-08ce-4602-bf5f-af5ef9647554-0' usage_metadata={'input_tokens': 94, 'output_tokens': 9, 'total_tokens': 103}
print('-'*30)

### 3. 세번째 질의: 내 이름이 뭐야?, session_id: 2a(다른 session_id) - 첫번 째 질의의  이름을 기억하지 못함
results = runnable_with_history.invoke(
    {"language": "Korean", "input": "whats my name?"},
    config={"configurable": {"session_id": "2a"}},
)
print(results)
# 출력
# content="Sorry, I don't have access to your name. How can I assist you today?" response_metadata={'token_usage': {'completion_tokens': 18, 'prompt_tokens': 32, 'total_tokens': 50}, 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None} id='run-9c7aaccc-4935-42bb-b4a8-4e676c79279b-0' usage_metadata={'input_tokens': 32, 'output_tokens': 18, 'total_tokens': 50}

