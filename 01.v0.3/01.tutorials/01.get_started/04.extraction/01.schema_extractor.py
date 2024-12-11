# pip install --upgrade langchain-core
from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from typing import Optional
from pydantic import BaseModel, Field


##################################################################################
### 1. The Schema
print('1.', '-' * 50)
##################################################################################

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
    
rprint(Person)  
# 1. --------------------------------------------------
# <class '__main__.Person'>
    
   
##################################################################################
### 2. The Extractor - PromptTemplate
print('2.', '-' * 50)
##################################################################################    
from typing import Optional

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Field

# Define a custom prompt to provide instructions and any additional context.
# 1) You can add examples into the prompt template to improve extraction quality
# 2) Introduce additional parameters to take context into account (e.g., include metadata
#    about the document from which the text was extracted.)
prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert extraction algorithm. "
            "Only extract relevant information from the text. "
            "If you do not know the value of an attribute asked to extract, "
            "return null for the attribute's value.",
        ),
        # Please see the how-to about improving performance with
        # reference examples.
        # MessagesPlaceholder('examples'),
        ("human", "{text}"),
    ]
)
rprint(prompt_template)
# 2. --------------------------------------------------
# ChatPromptTemplate(
#     input_variables=['text'],
#     input_types={},
#     partial_variables={},
#     messages=[
#         SystemMessagePromptTemplate(
#             prompt=PromptTemplate(
#                 input_variables=[],
#                 input_types={},
#                 partial_variables={},
#                 template="You are an expert extraction algorithm. Only extract relevant information from the text. If you do not know the value of an attribute asked to 
# extract, return null for the attribute's value."
#             ),
#             additional_kwargs={}
#         ),
#         HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=['text'], input_types={}, partial_variables={}, template='{text}'), additional_kwargs={})
#     ]
# )


##################################################################################
### 3. The Extractor - OpenAI
print('3.', '-' * 50)
##################################################################################    
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

structured_llm = llm.with_structured_output(schema=Person)

text = "Alan Smith is 6 feet tall and has blond hair."
prompt = prompt_template.invoke({"text": text})
results = structured_llm.invoke(prompt)
rprint(results)
# 3. --------------------------------------------------
# Person(name='Alan Smith', hair_color='blond', height_in_meters='1.83')
print(' ')
print(results.dict())
# {'name': 'Alan Smith', 'hair_color': 'blond', 'height_in_meters': '1.83'}
print(' ')
print(results.dict()['name'])
print(results.dict()['hair_color'])
print(results.dict()['height_in_meters'])
# Alan Smith
# blond
# 1.83
