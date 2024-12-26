from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)


#################################################################################
### 1. 제로샷 예제
print('1.', '-' * 50)
##################################################################################
rprint(model.invoke("What is 2 🦜 9?").content)
# 1. --------------------------------------------------
# The expression "2 🦜 9" seems to use a parrot emoji (🦜) in place of a mathematical operator. If you could clarify what operation you intend to represent with the parrot emoji, I would be happy to help you solve it!


#################################################################################
### 2. 퓨샷 예제 - 몇 개의 예제 제공
print('2.', '-' * 50)
##################################################################################
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

examples = [
    {"input": "2 🦜 2", "output": "4"},
    {"input": "2 🦜 3", "output": "5"},
]

# This is a prompt template used to format each individual example.
example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input}"),
        ("ai", "{output}"),
    ]
)
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
)

rprint(few_shot_prompt.invoke({}).to_messages())
# 2. --------------------------------------------------
# [
#     HumanMessage(content='2 🦜 2', additional_kwargs={}, response_metadata={}),
#     AIMessage(content='4', additional_kwargs={}, response_metadata={}),
#     HumanMessage(content='2 🦜 3', additional_kwargs={}, response_metadata={}),
#     AIMessage(content='5', additional_kwargs={}, response_metadata={})
# ]


#################################################################################
### 3. llm의 prompt에 적용 및 invoke
print('3.', '-' * 50)
##################################################################################
final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a wondrous wizard of math."),
        few_shot_prompt,
        ("human", "{input}"),
    ]
)

from langchain_openai import ChatOpenAI

chain = final_prompt | model

rprint(chain.invoke({"input": "What is 2 🦜 9?"}).content)
# 3. --------------------------------------------------
# 11