from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

##################################################################################
### 1. few-shot prompting
print('1.', '-' * 50)
##################################################################################
messages = [
    {"role": "user", "content": "2 🦜 2"},
    {"role": "assistant", "content": "4"},
    {"role": "user", "content": "2 🦜 3"},
    {"role": "assistant", "content": "5"},
    {"role": "user", "content": "3 🦜 4"},
]

response = llm.invoke(messages)
print(response.content)
# 7


##################################################################################
### 2. tool_example_to_messages: 도구를 호출하는 few-shot message 만들기
print('2.', '-' * 50)
##################################################################################
from langchain_core.utils.function_calling import tool_example_to_messages

from typing import List, Optional
from pydantic import BaseModel, Field
from rich import print as rprint

class Person(BaseModel):
    """Information about a person."""

    # ^ Doc-string for the entity Person.
    # This doc-string is sent to the LLM as the description of the schema Person,
    # and it can help to improve extraction results.

    # Note that:
    # 1. Each field is an `optional` -- this allows the model to decline to extract it!
    # 2. Each field has a `description` -- this description is used by the LLM.
    # Having a good description can help improve extraction results.
    name: Optional[str] = Field(default=None, description="The name of the person")
    hair_color: Optional[str] = Field(
        default=None, description="The color of the person's hair if known"
    )
    height_in_meters: Optional[str] = Field(
        default=None, description="Height measured in meters"
    )


class Data(BaseModel):
    """Extracted data about people."""

    # Creates a model so that we can extract multiple entities.
    people: List[Person]
    

examples = [
    (
        "The ocean is vast and blue. It's more than 20,000 feet deep.",
        Data(people=[]),
    ),
    (
        "Fiona traveled far from France to Spain.",
        Data(people=[Person(name="Fiona", height_in_meters=None, hair_color=None)]),
    ),
]


##################################################################################

messages = []

for txt, tool_call in examples:
    if tool_call.people:
        # This final message is optional for some providers
        ai_response = "Detected people."
    else:
        ai_response = "Detected no people."
    # print(f'tool_example_to_messages: {tool_example_to_messages(txt, [tool_call], ai_response=ai_response)}')
    messages.extend(tool_example_to_messages(txt, [tool_call], ai_response=ai_response))\
        
for message in messages:
    # message.pretty_print()
    print('-' * 10)
    rprint(message)
# 2. --------------------------------------------------
# /home/dev01/app/source_code/langchain_practice/01.v0.3/01.tutorials/01.get_started/04.extraction/03.reference_example.py:83: LangChainBetaWarning: The function `tool_example_to_messages` is in beta. It is actively being worked on, so the API may change.
#   messages.extend(tool_example_to_messages(txt, [tool_call], ai_response=ai_response))\
# ----------
# HumanMessage(content="The ocean is vast and blue. It's more than 20,000 feet deep.", additional_kwargs={}, response_metadata={})
# ----------
# AIMessage(
#     content='',
#     additional_kwargs={'tool_calls': [{'id': '1f86c766-9946-4029-bc01-fae3cefd847a', 'type': 'function', 'function': {'name': 'Data', 'arguments': '{"people":[]}'}}]},
#     response_metadata={},
#     tool_calls=[{'name': 'Data', 'args': {'people': []}, 'id': '1f86c766-9946-4029-bc01-fae3cefd847a', 'type': 'tool_call'}]
# )
# ----------
# ToolMessage(content='You have correctly called this tool.', tool_call_id='1f86c766-9946-4029-bc01-fae3cefd847a')
# ----------
# AIMessage(content='Detected no people.', additional_kwargs={}, response_metadata={})
# ----------
# HumanMessage(content='Fiona traveled far from France to Spain.', additional_kwargs={}, response_metadata={})
# ----------
# AIMessage(
#     content='',
#     additional_kwargs={
#         'tool_calls': [
#             {
#                 'id': 'fc0854e2-42b8-4ffd-9f06-4cb3f3d65e97',
#                 'type': 'function',
#                 'function': {'name': 'Data', 'arguments': '{"people":[{"name":"Fiona","hair_color":null,"height_in_meters":null}]}'}
#             }
#         ]
#     },
#     response_metadata={},
#     tool_calls=[
#         {
#             'name': 'Data',
#             'args': {'people': [{'name': 'Fiona', 'hair_color': None, 'height_in_meters': None}]},
#             'id': 'fc0854e2-42b8-4ffd-9f06-4cb3f3d65e97',
#             'type': 'tool_call'
#         }
#     ]
# )
# ----------
# ToolMessage(content='You have correctly called this tool.', tool_call_id='fc0854e2-42b8-4ffd-9f06-4cb3f3d65e97')
# ----------
# AIMessage(content='Detected people.', additional_kwargs={}, response_metadata={})    


##################################################################################
### 3. few-shot 없이 사용하기
print('3.', '-' * 50)
##################################################################################
message_no_extraction = {
    "role": "user",
    "content": "The solar system is large, but earth has only 1 moon.",
}

structured_llm = llm.with_structured_output(schema=Data)
results = structured_llm.invoke([message_no_extraction])
rprint(results)
# 3. --------------------------------------------------
# Data(people=[Person(name='Earth', hair_color='None', height_in_meters='0')])


##################################################################################
### 4. few-shot 을 포함하여 사용하기
print('4.', '-' * 50)
##################################################################################
results = structured_llm.invoke(messages + [message_no_extraction])
rprint(results)
# 4. --------------------------------------------------
# Data(people=[])