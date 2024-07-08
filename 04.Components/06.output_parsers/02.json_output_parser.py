from dotenv import load_dotenv
load_dotenv()

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI

model = ChatOpenAI(temperature=0)


# Define your desired data structure.
class Joke(BaseModel):
    setup: str = Field(description="question to set up a joke")
    punchline: str = Field(description="answer to resolve the joke")


# And a query intented to prompt a language model to populate the data structure.
joke_query = "Tell me a joke."

# Set up a parser + inject instructions into the prompt template.
parser = JsonOutputParser(pydantic_object=Joke)
print(f'parser.get_format_instructions(): {parser.get_format_instructions()}')
print('-'*30)
# parser.get_format_instructions(): The output should be formatted as a JSON instance that conforms to the JSON schema below.

# As an example, for the schema {"properties": {"foo": {"title": "Foo", "description": "a list of strings", "type": "array", "items": {"type": "string"}}}, "required": ["foo"]}
# the object {"foo": ["bar", "baz"]} is a well-formatted instance of the schema. The object {"properties": {"foo": ["bar", "baz"]}} is not well-formatted.

# Here is the output schema:
# ```
# {"properties": {"setup": {"title": "Setup", "description": "question to set up a joke", "type": "string"}, "punchline": {"title": "Punchline", "description": "answer to resolve the joke", "type": "string"}}, "required": ["setup", "punchline"]}
# ```

prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)


### 1. parser(JsonOutputParser) 적용
chain = prompt | model | parser

results = chain.invoke({"query": joke_query})
print(results)
# {'setup': "Why couldn't the bicycle stand up by itself?", 'punchline': 'Because it was two tired!'}


### 2. streaming 적용 - JsonOutputParser 이므로 사용 가능
print('-'*30)
for s in chain.stream({"query": joke_query}):
    print(s)
# {}
# {'setup': ''}
# {'setup': 'Why'}
# {'setup': 'Why couldn'}
# {'setup': "Why couldn't"}
# {'setup': "Why couldn't the"}
# {'setup': "Why couldn't the bicycle"}
# {'setup': "Why couldn't the bicycle stand"}
# {'setup': "Why couldn't the bicycle stand up"}
# {'setup': "Why couldn't the bicycle stand up by"}
# {'setup': "Why couldn't the bicycle stand up by itself"}
# {'setup': "Why couldn't the bicycle stand up by itself?"}
# {'setup': "Why couldn't the bicycle stand up by itself?", 'punchline': ''}
# {'setup': "Why couldn't the bicycle stand up by itself?", 'punchline': 'Because'}
# {'setup': "Why couldn't the bicycle stand up by itself?", 'punchline': 'Because it'}
# {'setup': "Why couldn't the bicycle stand up by itself?", 'punchline': 'Because it was'}
# {'setup': "Why couldn't the bicycle stand up by itself?", 'punchline': 'Because it was two'}
# {'setup': "Why couldn't the bicycle stand up by itself?", 'punchline': 'Because it was two tired'}
# {'setup': "Why couldn't the bicycle stand up by itself?", 'punchline': 'Because it was two tired!'}    


### 3. JsonOutputParser를 Pydantic 없이 사용
print('-'*30)
joke_query = "Tell me a joke."

parser = JsonOutputParser()
print(f'parser.get_format_instructions(): {parser.get_format_instructions()}')
print('-'*30)
# parser.get_format_instructions(): Return a JSON object.

prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt | model | parser

results = chain.invoke({"query": joke_query})
print(results)
# {'response': "Why couldn't the bicycle stand up by itself? Because it was two tired!"}