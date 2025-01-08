### string, dict를 input으로 하는 Runnable을 tool로 변경

from rich import print as rprint
from langchain_core.language_models import GenericFakeChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages(
    [("human", "Hello. Please respond in the style of {answer_style}.")]
)

# Placeholder LLM
llm = GenericFakeChatModel(messages=iter(["hello matey"]))
### 어떤 llm 인지 확인 하기 ###
# rprint(llm.invoke([("human", "Hello. Please respond in the style of {answer_style}.")]))
# AIMessage(content='hello matey', additional_kwargs={}, response_metadata={}, id='run-ca02f72f-f024-41db-aa14-f02e763b89f2-0')

### chain 확인 하기 ###
### 위의 llm을 invoke 하면 아래에서 error 발생 -> iter(["hello matey"] 라서 한 번 호출 되면 아마 호출의 return 값이 없어서 error 발생
chain = prompt | llm | StrOutputParser()
# rprint(chain.invoke({"answer_style": "pirate"}))
# hello matey

#################################################################################
### 1. string, dict를 input으로 하는 Runnable을 tool로 변경
###  chain.as_tool( => LangChainBetaWarning: This API is in beta and may change in the future.
print('1.', '-' * 50)
##################################################################################
as_tool = chain.as_tool(
    name="Style responder", description="Description of when to use tool."
)
rprint(as_tool.name)
rprint(as_tool.description)
rprint(as_tool.args)
print(' ')
rprint(as_tool.invoke({"answer_style": "pirate"}))
# Style responder
# Description of when to use tool.
# {'answer_style': {'title': 'Answer Style', 'type': 'string'}}
# 
# hello matey