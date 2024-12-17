from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

from rich import print as rprint


##################################################################################
### 1. 체인(chain)에 포함된 모든 프롬프트를 확인하는 방법
### prompt1: 기본적인 채팅 프롬프트
### prompt2: AI의 답변이 한 번 포함된 채팅 프롬프트
print('1.', '-' * 50)
##################################################################################
prompt1 = ChatPromptTemplate.from_messages(
    [("system", "good ai"), ("human", "{input}")]
)
prompt2 = ChatPromptTemplate.from_messages(
    [
        ("system", "really good ai"),
        ("human", "{input}"),
        ("ai", "{ai_output}"),
        ("human", "{input2}"),
    ]
)
fake_llm = RunnableLambda(lambda prompt: "i am good ai")
chain = prompt1.assign(ai_output=fake_llm) | prompt2 | fake_llm

for i, prompt in enumerate(chain.get_prompts()):
    print(f"**prompt {i=}**\n")
    print(prompt.pretty_repr())
    print("\n" * 3)
# 1. --------------------------------------------------
# **prompt i=0**

# ================================ System Message ================================

# good ai

# ================================ Human Message =================================

# {input}




# **prompt i=1**

# ================================ System Message ================================

# really good ai

# ================================ Human Message =================================

# {input}

# ================================== AI Message ==================================

# {ai_output}

# ================================ Human Message =================================

# {input2}


##################################################################################
### 2. 단계별 확인
### chain = prompt1.assign(ai_output=fake_llm) | prompt2 | fake_llm
print('2.', '-' * 50)
##################################################################################    
rprint(prompt1.assign(ai_output=fake_llm))
# 2. --------------------------------------------------
# RunnableSequence(
#     first=ChatPromptTemplate(
#         input_variables=['input'],
#         input_types={},
#         partial_variables={},
#         messages=[
#             SystemMessagePromptTemplate(prompt=PromptTemplate(input_variables=[], input_types={}, partial_variables={}, template='good ai'), additional_kwargs={}),
#             HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=['input'], input_types={}, partial_variables={}, template='{input}'), additional_kwargs={})
#         ]
#     ),
#     middle=[],
#     last=RunnableAssign(mapper=RunnableParallel[dict[str, Any]](steps__={'ai_output': RunnableLambda(lambda prompt: 'i am good ai')}))
# )

print(' ')
rprint(prompt1.assign(ai_output=fake_llm) | prompt2)
# RunnableSequence(
#     first=ChatPromptTemplate(
#         input_variables=['input'],
#         input_types={},
#         partial_variables={},
#         messages=[
#             SystemMessagePromptTemplate(prompt=PromptTemplate(input_variables=[], input_types={}, partial_variables={}, template='good ai'), additional_kwargs={}),
#             HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=['input'], input_types={}, partial_variables={}, template='{input}'), additional_kwargs={})
#         ]
#     ),
#     middle=[RunnableAssign(mapper=RunnableParallel[dict[str, Any]](steps__={'ai_output': RunnableLambda(lambda prompt: 'i am good ai')}))],
#     last=ChatPromptTemplate(
#         input_variables=['ai_output', 'input', 'input2'],
#         input_types={},
#         partial_variables={},
#         messages=[
#             SystemMessagePromptTemplate(prompt=PromptTemplate(input_variables=[], input_types={}, partial_variables={}, template='really good ai'), additional_kwargs={}),
#             HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=['input'], input_types={}, partial_variables={}, template='{input}'), additional_kwargs={}),
#             AIMessagePromptTemplate(prompt=PromptTemplate(input_variables=['ai_output'], input_types={}, partial_variables={}, template='{ai_output}'), additional_kwargs={}),
#             HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=['input2'], input_types={}, partial_variables={}, template='{input2}'), additional_kwargs={})
#         ]
#     )
# )


print(' ')
rprint(prompt1.assign(ai_output=fake_llm) | prompt2 | fake_llm)
# RunnableSequence(
#     first=ChatPromptTemplate(
#         input_variables=['input'],
#         input_types={},
#         partial_variables={},
#         messages=[
#             SystemMessagePromptTemplate(prompt=PromptTemplate(input_variables=[], input_types={}, partial_variables={}, template='good ai'), additional_kwargs={}),
#             HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=['input'], input_types={}, partial_variables={}, template='{input}'), additional_kwargs={})
#         ]
#     ),
#     middle=[
#         RunnableAssign(mapper=RunnableParallel[dict[str, Any]](steps__={'ai_output': RunnableLambda(lambda prompt: 'i am good ai')})),
#         ChatPromptTemplate(
#             input_variables=['ai_output', 'input', 'input2'],
#             input_types={},
#             partial_variables={},
#             messages=[
#                 SystemMessagePromptTemplate(prompt=PromptTemplate(input_variables=[], input_types={}, partial_variables={}, template='really good ai'), additional_kwargs={}),
#                 HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=['input'], input_types={}, partial_variables={}, template='{input}'), additional_kwargs={}),
#                 AIMessagePromptTemplate(prompt=PromptTemplate(input_variables=['ai_output'], input_types={}, partial_variables={}, template='{ai_output}'), additional_kwargs={}),
#                 HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=['input2'], input_types={}, partial_variables={}, template='{input2}'), additional_kwargs={})
#             ]
#         )
#     ],
#     last=RunnableLambda(lambda prompt: 'i am good ai')
# )


##################################################################################
### 3. invoke()
### chain = prompt1.assign(ai_output=fake_llm) | prompt2 | fake_llm
### invoke를 하기 위해 chain을 수정
print('3.', '-' * 50)
##################################################################################    
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

chain = (
    RunnableParallel(
        {
            "input": RunnablePassthrough(),
            "ai_output": prompt1 | fake_llm,
            "input2": lambda x: x["input2"]  # input2를 전달
        }
    )
    | prompt2
    | fake_llm
)

rprint(chain.invoke({"input": "hello", "input2": "How are you?"}))
# 3. --------------------------------------------------
# i am good ai