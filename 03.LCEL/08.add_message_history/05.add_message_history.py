from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import ConfigurableFieldSpec


def get_session_history(user_id: str, conversation_id: str):
    return SQLChatMessageHistory(f"{user_id}--{conversation_id}", connection="sqlite:///memory.db")

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

with_message_history = RunnableWithMessageHistory(
    runnable,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
    history_factory_config=[
        ConfigurableFieldSpec(
            id="user_id",
            annotation=str,
            name="User ID",
            description="Unique identifier for the user.",
            default="",
            is_shared=True,
        ),
        ConfigurableFieldSpec(
            id="conversation_id",
            annotation=str,
            name="Conversation ID",
            description="Unique identifier for the conversation.",
            default="",
            is_shared=True,
        ),
    ],
)

### 1. 첫번째 질의: 난 bob이야!, session_id: 1
results = with_message_history.invoke(
    {"language": "Korean", "input": "hi im bob!"},
    config={"configurable": {"user_id": "123", "conversation_id": "1"}},
)
print(results)
# 출력
# content='안녕하세요, 밥님! 무엇을 도와드릴까요?' response_metadata={'token_usage': {'completion_tokens': 26, 'prompt_tokens': 31, 'total_tokens': 57}, 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None} id='run-5a45f08b-1d0a-4dcb-ad05-4fb4c7e56238-0' usage_metadata={'input_tokens': 31, 'output_tokens': 26, 'total_tokens': 57}
print('-'*30)

### 2. 두번째 질의: 내 이름이 뭐야?, session_id: 1 - 첫번째 질의의 이름을 기억
results = with_message_history.invoke(
    {"language": "Korean", "input": "whats my name?"},
    config={"configurable": {"user_id": "123", "conversation_id": "1"}},
)
print(results)
# 출력
# content='당신의 이름은 "밥" 입니다. 어떻게 도와드릴까요?' response_metadata={'token_usage': {'completion_tokens': 28, 'prompt_tokens': 70, 'total_tokens': 98}, 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None} id='run-5a48ad2d-00d9-44b2-89f4-8aaf831f10fe-0' usage_metadata={'input_tokens': 70, 'output_tokens': 28, 'total_tokens': 98}
print('-'*30)

### 3. 세번째 질의: 내 이름이 뭐야?, session_id: 2a(다른 session_id) - 첫번 째 질의의  이름을 기억하지 못함
results = with_message_history.invoke(
    {"language": "Korean", "input": "whats my name?"},
    config={"configurable": {"user_id": "456", "conversation_id": "1"}},
)
print(results)
# 출력
# content="I'm sorry, I don't have access to personal information. How can I assist you today?" response_metadata={'token_usage': {'completion_tokens': 20, 'prompt_tokens': 32, 'total_tokens': 52}, 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None} id='run-9fc9790f-8cbc-455f-8b24-9a902e1c09a5-0' usage_metadata={'input_tokens': 32, 'output_tokens': 20, 'total_tokens': 52}
