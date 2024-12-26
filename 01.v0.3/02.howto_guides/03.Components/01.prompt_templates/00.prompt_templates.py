from rich import print as rprint

#################################################################################
### 1. String Prompt Templates
### 단일 문자열 - 채팅이 아님
print('1.', '-' * 50)
##################################################################################
from langchain_core.prompts import PromptTemplate

prompt_template = PromptTemplate.from_template("Tell me a joke about {topic}")
rprint(prompt_template)
# PromptTemplate(input_variables=['topic'], input_types={}, partial_variables={}, template='Tell me a joke about {topic}')

rprint(prompt_template.invoke({"topic": "cats"}))
# 1. --------------------------------------------------
# StringPromptValue(text='Tell me a joke about cats')


#################################################################################
### 2. Chat Prompt Templates
### 채팅 형식의 템플릿 - 메시지 목록
print('2.', '-' * 50)
##################################################################################
from langchain_core.prompts import ChatPromptTemplate

prompt_template = ChatPromptTemplate([
    ("system", "You are a helpful assistant"),
    ("user", "Tell me a joke about {topic}")
])
rprint(prompt_template)
# 2. --------------------------------------------------
# ChatPromptTemplate(
#     input_variables=['topic'],
#     input_types={},
#     partial_variables={},
#     messages=[
#         SystemMessagePromptTemplate(prompt=PromptTemplate(input_variables=[], input_types={}, partial_variables={}, template='You are a helpful assistant'), additional_kwargs={}),
#         HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=['topic'], input_types={}, partial_variables={}, template='Tell me a joke about {topic}'), additional_kwargs={})
#     ]
# )

rprint(prompt_template.invoke({"topic": "cats"}))
# ChatPromptValue(messages=[SystemMessage(content='You are a helpful assistant', additional_kwargs={}, response_metadata={}), HumanMessage(content='Tell me a joke about cats', additional_kwargs={}, response_metadata={})])


#################################################################################
### 3. MessagePlaceholder
### MessagesPlaceholder: 특정 위치에 메시지 목록을 추가하는 역할
print('3.', '-' * 50)
##################################################################################
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage

prompt_template = ChatPromptTemplate([
    ("system", "You are a helpful assistant"),
    MessagesPlaceholder("msgs")
])
rprint(prompt_template)
# 3. --------------------------------------------------
# ChatPromptTemplate(
#     input_variables=['msgs'],
#     input_types={
#         'msgs': list[typing.Annotated[typing.Union[typing.Annotated[langchain_core.messages.ai.AIMessage, Tag(tag='ai')], typing.Annotated[langchain_core.messages.human.HumanMessage, Tag(tag='human')], 
# typing.Annotated[langchain_core.messages.chat.ChatMessage, Tag(tag='chat')], typing.Annotated[langchain_core.messages.system.SystemMessage, Tag(tag='system')], typing.Annotated[langchain_core.messages.function.FunctionMessage,
# Tag(tag='function')], typing.Annotated[langchain_core.messages.tool.ToolMessage, Tag(tag='tool')], typing.Annotated[langchain_core.messages.ai.AIMessageChunk, Tag(tag='AIMessageChunk')], 
# typing.Annotated[langchain_core.messages.human.HumanMessageChunk, Tag(tag='HumanMessageChunk')], typing.Annotated[langchain_core.messages.chat.ChatMessageChunk, Tag(tag='ChatMessageChunk')], 
# typing.Annotated[langchain_core.messages.system.SystemMessageChunk, Tag(tag='SystemMessageChunk')], typing.Annotated[langchain_core.messages.function.FunctionMessageChunk, Tag(tag='FunctionMessageChunk')], 
# typing.Annotated[langchain_core.messages.tool.ToolMessageChunk, Tag(tag='ToolMessageChunk')]], FieldInfo(annotation=NoneType, required=True, discriminator=Discriminator(discriminator=<function _get_type at 0x756394c55990>, 
# custom_error_type=None, custom_error_message=None, custom_error_context=None))]]
#     },
#     partial_variables={},
#     messages=[
#         SystemMessagePromptTemplate(prompt=PromptTemplate(input_variables=[], input_types={}, partial_variables={}, template='You are a helpful assistant'), additional_kwargs={}),
#         MessagesPlaceholder(variable_name='msgs')
#     ]
# )

rprint(prompt_template.invoke({"msgs": [HumanMessage(content="hi!")]}))
# ChatPromptValue(messages=[SystemMessage(content='You are a helpful assistant', additional_kwargs={}, response_metadata={}), HumanMessage(content='hi!', additional_kwargs={}, response_metadata={})])


#################################################################################
### 4. MessagePlaceholder
### MessagesPlaceholder의 다른 방법
print('4.', '-' * 50)
##################################################################################
prompt_template = ChatPromptTemplate([
    ("system", "You are a helpful assistant"),
    ("placeholder", "{msgs}") # <-- This is the changed part
])

rprint(prompt_template.invoke({"msgs": [HumanMessage(content="hi!")]}))
# 4. --------------------------------------------------
# ChatPromptValue(messages=[SystemMessage(content='You are a helpful assistant', additional_kwargs={}, response_metadata={}), HumanMessage(content='hi!', additional_kwargs={}, response_metadata={})])