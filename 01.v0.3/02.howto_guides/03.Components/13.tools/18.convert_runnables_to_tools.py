# pip install -U langchain-core langchain-openai langgraph

# LangChain 도구는 에이전트, 체인 또는 채팅 모델이 외부 세계와 상호작용하기 위해 사용할 수 있는 인터페이스입니다. 
# LangChain 도구(BaseTool의 인스턴스)는 언어 모델이 효과적으로 호출할 수 있도록 추가 제약 조건이 있는 Runnable입니다:

# 입력은 직렬화 가능한 것으로 제한되며, 구체적으로 문자열과 Python 딕셔너리 객체입니다;
# 사용 방법과 시기를 나타내는 이름과 설명이 포함되어 있습니다;
# 인수에 대한 상세한 args_schema가 포함될 수 있습니다. 즉, 도구(Runnable로서)가 단일 딕셔너리 입력을 받을 수 있지만, 딕셔너리를 채우는 데 필요한 특정 키와 타입 정보는 args_schema에 명시되어야 합니다.

# 문자열이나 딕셔너리 입력을 받는 Runnable은 as_tool 메서드를 사용하여 도구로 변환할 수 있으며, 이를 통해 이름, 설명 및 인수에 대한 추가 스키마 정보를 지정할 수 있습니다.

from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

import random
from typing import List, Tuple

from langchain_core.tools import tool

#################################################################################
### 1. Basic usage
#################################################################################

#################################################################################
### 1-1. typed dict를 input으로
print('1-1.', '-' * 50)
################################################################################## 
from typing import List

from langchain_core.runnables import RunnableLambda
from typing_extensions import TypedDict


class Args(TypedDict):
    a: int
    b: List[int]


def f(x: Args) -> str:
    return str(x["a"] * max(x["b"]))


runnable = RunnableLambda(f)
as_tool = runnable.as_tool(
    name="My tool",
    description="Explanation of when to use tool.",
)
rprint(as_tool)
### LangChainBetaWarning: This API is in beta and may change in the future.   as_tool = runnable.as_tool(
# 1-1. --------------------------------------------------
# StructuredTool(
#     name='My tool',
#     description='Explanation of when to use tool.',
#     args_schema=<class 'langchain_core.tools.convert.My tool'>,
#     func=<function convert_runnable_to_tool.<locals>.invoke_wrapper at 0x7a5e3dee5fc0>,
#     coroutine=<function convert_runnable_to_tool.<locals>.ainvoke_wrapper at 0x7a5e3dee5360>
# )

print(' ')
rprint(as_tool.invoke({"a": 3, "b": [1, 2]}))
# 6


#################################################################################
### 1-2. 타입 정보를 입력하지 않고도 arg_types를 통해 인자 타입을 지정
print('1-2.', '-' * 50)
################################################################################## 
from typing import Any, Dict


def g(x: Dict[str, Any]) -> str:
    return str(x["a"] * max(x["b"]))


runnable = RunnableLambda(g)
as_tool = runnable.as_tool(
    name="My tool",
    description="Explanation of when to use tool.",
    arg_types={"a": int, "b": List[int]},
)
rprint(as_tool)
# 1-2. --------------------------------------------------
# StructuredTool(
#     name='My tool',
#     description='Explanation of when to use tool.',
#     args_schema=<class 'langchain_core.tools.convert.My tool'>,
#     func=<function convert_runnable_to_tool.<locals>.invoke_wrapper at 0x77426e1148b0>,
#     coroutine=<function convert_runnable_to_tool.<locals>.ainvoke_wrapper at 0x77426e06fbe0>
# )
print(' ')
rprint(as_tool.invoke({"a": 3, "b": [1, 2]}))
# 6


#################################################################################
### 1-3. 대안으로, 도구에 대한 args_schema를 직접 전달하여 스키마를 완전히 지정
print('1-3.', '-' * 50)
################################################################################## 
from pydantic import BaseModel, Field


class GSchema(BaseModel):
    """Apply a function to an integer and list of integers."""

    a: int = Field(..., description="Integer")
    b: List[int] = Field(..., description="List of ints")


runnable = RunnableLambda(g)
as_tool = runnable.as_tool(GSchema)
rprint(as_tool)
# 1-3. --------------------------------------------------
# StructuredTool(
#     name='g',
#     description="Takes {'description': 'Apply a function to an integer and list of integers.', 'properties': {'a': {'description': 'Integer', 'title': 'A', 'type': 'integer'}, 'b': {'description': 'List of 
# ints', 'items': {'type': 'integer'}, 'title': 'B', 'type': 'array'}}, 'required': ['a', 'b'], 'title': 'GSchema', 'type': 'object'}.",
#     args_schema=<class '__main__.GSchema'>,
#     func=<function convert_runnable_to_tool.<locals>.invoke_wrapper at 0x7235d2821240>,
#     coroutine=<function convert_runnable_to_tool.<locals>.ainvoke_wrapper at 0x7235d2821120>
# )
print(' ')
rprint(as_tool.invoke({"a": 3, "b": [1, 2]}))
# 6


#################################################################################
### 1-4. string 입력도 지원
print('1-4.', '-' * 50)
################################################################################## 
def f(x: str) -> str:
    return x + "a"


def g(x: str) -> str:
    return x + "z"


runnable = RunnableLambda(f) | g
as_tool = runnable.as_tool()
rprint(as_tool)

print(' ')
rprint(as_tool.invoke("b"))
# baz


#################################################################################
### 2. In agents
#################################################################################
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

#################################################################################
### RAG tutorial - retriever 구성
################################################################################## 
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings

documents = [
    Document(
        page_content="Dogs are great companions, known for their loyalty and friendliness.",
    ),
    Document(
        page_content="Cats are independent pets that often enjoy their own space.",
    ),
]

vectorstore = InMemoryVectorStore.from_documents(
    documents, embedding=OpenAIEmbeddings()
)

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 1},
)
# rprint(retriever)


#################################################################################
### 사전 구축된 LangGraph agent에 tool을 제공
################################################################################## 
from langgraph.prebuilt import create_react_agent

tools = [
    retriever.as_tool(
        name="pet_info_retriever",
        description="Get information about pets.",
    )
]
agent = create_react_agent(llm, tools)
# rprint(agent)


#################################################################################
### 2-1. streaming
### 공식문서와 다르게 나옴 => {'agent': -> {'tools': -> {'agent':
### 실습: {'agent': 만 나옴
print('2-1.', '-' * 50)
################################################################################## 
for chunk in agent.stream({"messages": [("human", "What are dogs known for?")]}):
    rprint(chunk)
    print("****")
# 2-1. --------------------------------------------------
# {
#     'agent': {
#         'messages': [
#             AIMessage(
#                 content='Dogs are known for a variety of qualities and traits, including:\n\n1. **Loyalty**: Dogs are often referred to as "man\'s best friend" due to their strong loyalty to their owners and 
# families.\n\n2. **Companionship**: They provide companionship and emotional support, helping to reduce feelings of loneliness and depression.\n\n3. **Intelligence**: Many dog breeds are known for their 
# intelligence and ability to learn commands, tricks, and tasks.\n\n4. **Protectiveness**: Dogs can be protective of their owners and homes, often serving as guardians.\n\n5. **Sociability**: Dogs are generally 
# social animals that enjoy interacting with humans and other dogs.\n\n6. **Variety of Breeds**: There are hundreds of dog breeds, each with unique characteristics, sizes, and temperaments.\n\n7. **Working 
# Roles**: Dogs serve in various working roles, including service dogs for the disabled, therapy dogs, police and military dogs, and search and rescue dogs.\n\n8. **Playfulness**: Dogs are known for their playful
# nature and love for games, such as fetch and tug-of-war.\n\n9. **Senses**: Dogs have an exceptional sense of smell and hearing, often used in tracking, hunting, and detection roles.\n\n10. **Affection**: Dogs 
# are known for their affectionate behavior, showing love and attachment to their owners through cuddling, licking, and following them around.\n\nThese qualities contribute to their popularity as pets and working
# animals in various settings.',
#                 additional_kwargs={'refusal': None},
#                 response_metadata={
#                     'token_usage': {
#                         'completion_tokens': 304,
#                         'prompt_tokens': 58,
#                         'total_tokens': 362,
#                         'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#                         'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
#                     },
#                     'model_name': 'gpt-4o-mini-2024-07-18',
#                     'system_fingerprint': 'fp_f2cd28694a',
#                     'finish_reason': 'stop',
#                     'logprobs': None
#                 },
#                 id='run-e7ed5a84-5408-4f2d-80b5-7956232a7d05-0',
#                 usage_metadata={'input_tokens': 58, 'output_tokens': 304, 'total_tokens': 362, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
#             )
#         ]
#     }
# }
# ****    

### 공식문서 ###
# {'agent': {'messages': [AIMessage(content='', additional_kwargs={'tool_calls': [{'id': 'call_W8cnfOjwqEn4cFcg19LN9mYD', 'function': {'arguments': '{"__arg1":"dogs"}', 'name': 'pet_info_retriever'}, 'type': 'function'}]}, response_metadata={'token_usage': {'completion_tokens': 19, 'prompt_tokens': 60, 'total_tokens': 79}, 'model_name': 'gpt-4o-mini', 'system_fingerprint': None, 'finish_reason': 'tool_calls', 'logprobs': None}, id='run-d7f81de9-1fb7-4caf-81ed-16dcdb0b2ab4-0', tool_calls=[{'name': 'pet_info_retriever', 'args': {'__arg1': 'dogs'}, 'id': 'call_W8cnfOjwqEn4cFcg19LN9mYD'}], usage_metadata={'input_tokens': 60, 'output_tokens': 19, 'total_tokens': 79})]}}
# ----
# {'tools': {'messages': [ToolMessage(content="[Document(id='86f835fe-4bbe-4ec6-aeb4-489a8b541707', page_content='Dogs are great companions, known for their loyalty and friendliness.')]", name='pet_info_retriever', tool_call_id='call_W8cnfOjwqEn4cFcg19LN9mYD')]}}
# ----
# {'agent': {'messages': [AIMessage(content='Dogs are known for being great companions, known for their loyalty and friendliness.', response_metadata={'token_usage': {'completion_tokens': 18, 'prompt_tokens': 134, 'total_tokens': 152}, 'model_name': 'gpt-4o-mini', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None}, id='run-9ca5847a-a5eb-44c0-a774-84cc2c5bbc5b-0', usage_metadata={'input_tokens': 134, 'output_tokens': 18, 'total_tokens': 152})]}}
# ----


#################################################################################
### 2-2. simple RAG chain 구성 - answer_style 추가
################################################################################## 
from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

system_prompt = """
You are an assistant for question-answering tasks.
Use the below context to answer the question. If
you don't know the answer, say you don't know.
Use three sentences maximum and keep the answer
concise.

Answer in the style of {answer_style}.

Question: {question}

Context: {context}
"""

prompt = ChatPromptTemplate.from_messages([("system", system_prompt)])

rag_chain = (
    {
        "context": itemgetter("question") | retriever,
        "question": itemgetter("question"),
        "answer_style": itemgetter("answer_style"),
    }
    | prompt
    | llm
    | StrOutputParser()
)


#################################################################################
### 2-2-1. chain의 input_schema 확인
print('2-2-1.', '-' * 50)
################################################################################## 
rprint(rag_chain.input_schema.model_json_schema())
# 2-2-1. --------------------------------------------------
# {
#     'properties': {'question': {'title': 'Question'}, 'answer_style': {'title': 'Answer Style'}},
#     'required': ['question', 'answer_style'],
#     'title': 'RunnableParallel<context,question,answer_style>Input',
#     'type': 'object'
# }

#################################################################################
### chain을 tool로 변환하고 agent에 추가
################################################################################## 
rag_tool = rag_chain.as_tool(
    name="pet_expert",
    description="Get information about pets.",
)

agent = create_react_agent(llm, [rag_tool])

#################################################################################
### 2-2-2. agent에 streaming
print('2-2-2.', '-' * 50)
################################################################################## 
for chunk in agent.stream(
    {"messages": [("human", "What would a pirate say dogs are known for?")]}
):
    rprint(chunk)
    print("****")
# 2-2-2. --------------------------------------------------
# {
#     'agent': {
#         'messages': [
#             AIMessage(
#                 content='',
#                 additional_kwargs={
#                     'tool_calls': [
#                         {
#                             'id': 'call_DzjE3i2Gtwcl9UyayN8tPwqa',
#                             'function': {'arguments': '{"question":"What would a pirate say dogs are known for?","answer_style":"pirate"}', 'name': 'pet_expert'},
#                             'type': 'function'
#                         }
#                     ],
#                     'refusal': None
#                 },
#                 response_metadata={
#                     'token_usage': {
#                         'completion_tokens': 31,
#                         'prompt_tokens': 58,
#                         'total_tokens': 89,
#                         'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#                         'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
#                     },
#                     'model_name': 'gpt-4o-mini-2024-07-18',
#                     'system_fingerprint': 'fp_f2cd28694a',
#                     'finish_reason': 'tool_calls',
#                     'logprobs': None
#                 },
#                 id='run-5d9194d8-76bf-4599-9754-a4595124f6ff-0',
#                 tool_calls=[{'name': 'pet_expert', 'args': {'question': 'What would a pirate say dogs are known for?', 'answer_style': 'pirate'}, 'id': 'call_DzjE3i2Gtwcl9UyayN8tPwqa', 'type': 'tool_call'}],
#                 usage_metadata={'input_tokens': 58, 'output_tokens': 31, 'total_tokens': 89, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
#             )
#         ]
#     }
# }
# ****
# {
#     'tools': {
#         'messages': [
#             ToolMessage(
#                 content="Arrr, matey! Dogs be known fer their loyalty and friendliness, always stickin' by yer side like a trusty shipmate. Aye, they be the best companions on the high seas!",
#                 name='pet_expert',
#                 id='6520087e-56da-4794-801b-e44c6131488f',
#                 tool_call_id='call_DzjE3i2Gtwcl9UyayN8tPwqa'
#             )
#         ]
#     }
# }
# ****
# {
#     'agent': {
#         'messages': [
#             AIMessage(
#                 content="Arrr, matey! A pirate would say that dogs be known fer their loyalty and friendliness, always stickin' by yer side like a trusty shipmate. Aye, they be the best companions on the high 
# seas!",
#                 additional_kwargs={'refusal': None},
#                 response_metadata={
#                     'token_usage': {
#                         'completion_tokens': 48,
#                         'prompt_tokens': 138,
#                         'total_tokens': 186,
#                         'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#                         'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
#                     },
#                     'model_name': 'gpt-4o-mini-2024-07-18',
#                     'system_fingerprint': 'fp_01aeff40ea',
#                     'finish_reason': 'stop',
#                     'logprobs': None
#                 },
#                 id='run-ab3faf49-aad4-4a4f-9e11-a2c3f8b0e56c-0',
#                 usage_metadata={'input_tokens': 138, 'output_tokens': 48, 'total_tokens': 186, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
#             )
#         ]
#     }
# }
# ****    