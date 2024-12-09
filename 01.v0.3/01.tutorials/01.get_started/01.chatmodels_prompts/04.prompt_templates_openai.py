from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from langchain_openai import ChatOpenAI
# from langchain_anthropic import ChatAnthropic

from langchain_core.prompts import ChatPromptTemplate

system_template = "Translate the following from English into {language}"

prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user", "{text}")]
)
##################################################################################
### 1. PromptTemplate
print('1', '*'*50)
##################################################################################
rprint(prompt_template)
# 1 **************************************************
# ChatPromptTemplate(
#     input_variables=['language', 'text'],
#     input_types={},
#     partial_variables={},
#     messages=[
#         SystemMessagePromptTemplate(
#             prompt=PromptTemplate(input_variables=['language'], input_types={}, partial_variables={}, template='Translate the following from English into {language}'),
#             additional_kwargs={}
#         ),
#         HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=['text'], input_types={}, partial_variables={}, template='{text}'), additional_kwargs={})
#     ]
# )


##################################################################################
### 2. PromptTemplate Invoke 하기
print('2', '*'*50)
##################################################################################
prompt = prompt_template.invoke({"language": "Korean", "text": "hi!"})
rprint(prompt)
# 2 **************************************************
# ChatPromptValue(
#     messages=[
#         SystemMessage(content='Translate the following from English into Korean', additional_kwargs={}, response_metadata={}),
#         HumanMessage(content='hi!', additional_kwargs={}, response_metadata={})
#     ]
# )


##################################################################################
### 3. PromptTemplate의 messages 가져오기
print('3', '*'*50)
##################################################################################
rprint(prompt.to_messages())
# 3 **************************************************
# [
#   SystemMessage(content='Translate the following from English into Korean', additional_kwargs={}, response_metadata={}), 
#   HumanMessage(content='hi!', additional_kwargs={}, response_metadata={})
# ]


##################################################################################
### 4. model invoke 하기
print('4', '*'*50)
##################################################################################
model = ChatOpenAI(model="gpt-4o-mini")
response = model.invoke(prompt)
rprint(response.content)
# 4 **************************************************
# 안녕하세요!