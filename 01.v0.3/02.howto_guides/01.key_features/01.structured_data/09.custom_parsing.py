import json
import re
from typing import List

from langchain_core.messages import AIMessage
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


# Prompt
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Answer the user query. Output your answer as JSON that  "
            "matches the given schema: \`\`\`json\n{schema}\n\`\`\`. "
            "Make sure to wrap the answer in \`\`\`json and \`\`\` tags",
        ),
        ("human", "{query}"),
    ]
).partial(schema=People.schema())


# Custom parser
def extract_json(message: AIMessage) -> List[dict]:
    """Extracts JSON content from a string where JSON is embedded between \`\`\`json and \`\`\` tags.

    Parameters:
        text (str): The text containing the JSON content.

    Returns:
        list: A list of extracted JSON strings.
    """
    text = message.content
    # Define the regular expression pattern to match JSON blocks
    pattern = r"\`\`\`json(.*?)\`\`\`"

    # Find all non-overlapping matches of the pattern in the string
    matches = re.findall(pattern, text, re.DOTALL)

    # Return the list of matched JSON strings, stripping any leading or trailing whitespace
    try:
        return [json.loads(match.strip()) for match in matches]
    except Exception:
        raise ValueError(f"Failed to parse: {message}")
    
    
##################################################################################
### 1. Prompt 출력
print('1.', '-' * 50)
##################################################################################
query = "Anna is 23 years old and she is 6 feet tall"

print(prompt.format_prompt(query=query).to_string())
# 1. --------------------------------------------------
# System: Answer the user query. Output your answer as JSON that  matches the given schema: \`\`\`json
# {'$defs': {'Person': {'description': 'Information about a person.', 'properties': {'name': {'description': 'The name of the person', 'title': 'Name', 'type': 'string'}, 'height_in_meters': {'description': 'The height of the person expressed in meters.', 'title': 'Height In Meters', 'type': 'number'}}, 'required': ['name', 'height_in_meters'], 'title': 'Person', 'type': 'object'}}, 'description': 'Identifying information about all people in a text.', 'properties': {'people': {'items': {'$ref': '#/$defs/Person'}, 'title': 'People', 'type': 'array'}}, 'required': ['people'], 'title': 'People', 'type': 'object'}
# \`\`\`. Make sure to wrap the answer in \`\`\`json and \`\`\` tags
# Human: Anna is 23 years old and she is 6 feet tall


##################################################################################
### 2. 최종적으로 extract_json을 사용하여 결과 출력
print('2.', '-' * 50)
##################################################################################
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")
chain = prompt | llm | extract_json

results = chain.invoke({"query": query})
print(results)
# 2. --------------------------------------------------
# [{'people': [{'name': 'Anna', 'height_in_meters': 1.8288}]}]