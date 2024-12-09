from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage


### 첫번째 방법
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant"),
    MessagesPlaceholder("msgs")
])

results = prompt_template.invoke({"msgs": [HumanMessage(content="hi!")]})
print(results)
# messages=[SystemMessage(content='You are a helpful assistant'), HumanMessage(content='hi!')]


### 두번째 방법
print('-'*30)
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant"),
    ("placeholder", "{msgs}")
])

results = prompt_template.invoke({"msgs": [HumanMessage(content="hi!")]})
print(results)
# messages=[SystemMessage(content='You are a helpful assistant'), HumanMessage(content='hi!')]


### 2개 이상 가능? => 가능
print('-'*30)
prompt_template2 = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant"),
    MessagesPlaceholder("human_msgs"),
    MessagesPlaceholder("ai_msgs")
])

results = prompt_template2.invoke({"human_msgs": [HumanMessage(content="hi!")], "ai_msgs": [AIMessage(content="Hello! How can I assist you today?!")]})
print(results)
# messages=[SystemMessage(content='You are a helpful assistant'), HumanMessage(content='hi!'), AIMessage(content='Hello! How can I assist you today?!')]fa
