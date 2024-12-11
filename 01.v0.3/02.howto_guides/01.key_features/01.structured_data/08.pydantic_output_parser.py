from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from typing import List

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field


class Person(BaseModel):
    """Information about a person."""

    name: str = Field(..., description="The name of the person")
    height_in_meters: float = Field(
        ..., description="The height of the person expressed in meters."
    )


class People(BaseModel):
    """Identifying information about all people in a text."""

    people: List[Person]


# Set up a parser
parser = PydanticOutputParser(pydantic_object=People)

# Prompt
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Answer the user query. Wrap the output in `json` tags\n{format_instructions}",
        ),
        ("human", "{query}"),
    ]
).partial(format_instructions=parser.get_format_instructions())


query = "Anna is 23 years old and she is 6 feet tall"

##################################################################################
### 1. Prompt 출력
print('1.', '-' * 50)
##################################################################################
print(prompt.invoke({"query": query}).to_string())
# System: Answer the user query. Wrap the output in `json` tags
# The output should be formatted as a JSON instance that conforms to the JSON schema below.

# As an example, for the schema {"properties": {"foo": {"title": "Foo", "description": "a list of strings", "type": "array", "items": {"type": "string"}}}, "required": ["foo"]}
# the object {"foo": ["bar", "baz"]} is a well-formatted instance of the schema. The object {"properties": {"foo": ["bar", "baz"]}} is not well-formatted.

# Here is the output schema:
# ```
# {"$defs": {"Person": {"description": "Information about a person.", "properties": {"name": {"description": "The name of the person", "title": "Name", "type": "string"}, 
# "height_in_meters": {"description": "The height of the person expressed in meters.", "title": "Height In Meters", "type": "number"}}, "required": ["name", "height_in_meters"], 
# "title": "Person", "type": "object"}}, "description": "Identifying information about all people in a text.", "properties": {"people": {"items": {"$ref": "#/$defs/Person"}, 
# "title": "People", "type": "array"}}, "required": ["people"]}
# ```
# Human: Anna is 23 years old and she is 6 feet tall


##################################################################################
### 2. 최종적으로 parser를 사용하여 결과 출력
print('2.', '-' * 50)
##################################################################################
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")
chain = prompt | llm | parser

results = chain.invoke({"query": query})
rprint(results)
# 2. --------------------------------------------------
# People(people=[Person(name='Anna', height_in_meters=1.8288)])