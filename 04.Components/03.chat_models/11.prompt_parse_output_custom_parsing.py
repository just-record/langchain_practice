from dotenv import load_dotenv
load_dotenv()

import json
import re
from typing import List

from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI


class Person(BaseModel):
    """Information about a person."""

    name: str = Field(..., description="The name of the person")
    height_in_meters: float = Field(
        ..., description="The height of the person expressed in meters."
    )


class People(BaseModel):
    """Identifying information about all people in a text."""

    people: List[Person]


# Prompt
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Answer the user query. Output your answer as JSON that  "
            "matches the given schema: ```json\n{schema}\n```. "
            "Make sure to wrap the answer in ```json and ``` tags",
        ),
        ("human", "{query}"),
    ]
).partial(schema=People.schema())


# Custom parser
def extract_json(message: AIMessage) -> List[dict]:
    """Extracts JSON content from a string where JSON is embedded between ```json and ``` tags.

    Parameters:
        text (str): The text containing the JSON content.

    Returns:
        list: A list of extracted JSON strings.
    """
    text = message.content
    # Define the regular expression pattern to match JSON blocks
    pattern = r"```json(.*?)```"

    # Find all non-overlapping matches of the pattern in the string
    matches = re.findall(pattern, text, re.DOTALL)

    # Return the list of matched JSON strings, stripping any leading or trailing whitespace
    try:
        return [json.loads(match.strip()) for match in matches]
    except Exception:
        raise ValueError(f"Failed to parse: {message}")
    

query = "Anna is 23 years old and she is 6 feet tall"

print(prompt.format_prompt(query=query).to_string())
# System: Answer the user query. Output your answer as JSON that  matches the given schema: ```json
# {'title': 'People', 'description': 'Identifying information about all people in a text.', 'type': 'object', 'properties': {'people': {'title': 'People', 'type': 'array', 'items': {'$ref': '#/definitions/Person'}}}, 'required': ['people'], 'definitions': {'Person': {'title': 'Person', 'description': 'Information about a person.', 'type': 'object', 'properties': {'name': {'title': 'Name', 'description': 'The name of the person', 'type': 'string'}, 'height_in_meters': {'title': 'Height In Meters', 'description': 'The height of the person expressed in meters.', 'type': 'number'}}, 'required': ['name', 'height_in_meters']}}}
# ```. Make sure to wrap the answer in ```json and ``` tags
# Human: Anna is 23 years old and she is 6 feet tall


### Use with an chat model
print('-'*30)
chain = prompt | ChatOpenAI(model="gpt-3.5-turbo") | extract_json

results = chain.invoke({"query": query})
print(results)
# [{'title': 'People', 'description': 'Identifying information about all people in a text.', 'type': 'object', 'properties': {'people': {'title': 'People', 'type': 'array', 'items': {'$ref': '#/definitions/Person'}}}, 'required': ['people'], 'definitions': {'Person': {'title': 'Person', 'description': 'Information about a person.', 'type': 'object', 'properties': {'name': {'title': 'Name', 'description': 'The name of the person', 'type': 'string'}, 'height_in_meters': {'title': 'Height In Meters', 'description': 'The height of the person expressed in meters.', 'type': 'number'}}, 'required': ['name', 'height_in_meters']}}}]
### 원하는 답변이 나오지 않음
### [{'people': [{'name': 'Anna', 'height_in_meters': 1.8288}]}]


### chain = prompt | ChatOpenAI(model="gpt-3.5-turbo") 일 때
# ```json\n{\n    "title": "People",\n    "description": "Identifying information about all people in a text.",\n    "type": "object",\n    "properties": {\n        "people": {\n            "title": "People",\n            "type": "array",\n            "items": {\n                "$ref": "#/definitions/Person"\n            }\n        }\n    },\n    "required": ["people"],\n    "definitions": {\n        "Person": {\n            "title": "Person",\n            "description": "Information about a person.",\n            "type": "object",\n            "properties": {\n                "name": {\n                    "title": "Name",\n                    "description": "The name of the person",\n                    "type": "string"\n                },\n                "height_in_meters": {\n                    "title": "Height In Meters",\n                    "description": "The height of the person expressed in meters.",\n                    "type": "number"\n                }\n            },\n            "required": ["name", "height_in_meters"]\n        }\n    }\n}\n```'