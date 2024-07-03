from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage


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
    MessagesPlaceholder("msgs"),
    MessagesPlaceholder("msgs2")
])

results = prompt_template2.invoke({"msgs": [HumanMessage(content="hi!")], "msgs2": [HumanMessage(content="hi2!")]})
print(results)
# messages=[SystemMessage(content='You are a helpful assistant'), HumanMessage(content='hi!'), HumanMessage(content='hi2!')]
