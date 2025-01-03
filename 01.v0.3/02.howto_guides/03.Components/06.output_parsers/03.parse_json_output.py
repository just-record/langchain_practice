# 출력 파서를 사용하여 사용자가 프롬프트를 통해 임의의 JSON 스키마를 지정하고, 해당 스키마를 준수하는 출력을 모델에 쿼리한 다음, 그 스키마를 JSON으로 파싱
from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint


#################################################################################
### 1. Pydantic을 사용한 JsonOutputParser 예시
### 파서에서 format_instructions를 프롬프트에 직접 전달
print('1.', '-' * 50)
##################################################################################
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

model = ChatOpenAI(temperature=0)


# Define your desired data structure.
class Joke(BaseModel):
    setup: str = Field(description="question to set up a joke")
    punchline: str = Field(description="answer to resolve the joke")


# And a query intented to prompt a language model to populate the data structure.
joke_query = "Tell me a joke."

# Set up a parser + inject instructions into the prompt template.
parser = JsonOutputParser(pydantic_object=Joke)

prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt | model | parser

rprint(chain.invoke({"query": joke_query}))
# 1. --------------------------------------------------
# {'setup': "Why couldn't the bicycle stand up by itself?", 'punchline': 'Because it was two tired!'}

### parser.get_format_instructions() ###
print('')
rprint(parser.get_format_instructions())
# The output should be formatted as a JSON instance that conforms to the JSON schema below.

# As an example, for the schema {"properties": {"foo": {"title": "Foo", "description": "a list of strings", "type": "array", "items": {"type": "string"}}}, "required": ["foo"]}
# the object {"foo": ["bar", "baz"]} is a well-formatted instance of the schema. The object {"properties": {"foo": ["bar", "baz"]}} is not well-formatted.

# Here is the output schema:
# ```
# {"properties": {"setup": {"description": "question to set up a joke", "title": "Setup", "type": "string"}, "punchline": {"description": "answer to resolve the joke", "title": "Punchline", "type": "string"}}, "required": 
# ["setup", "punchline"]}
# ```

### parser ###
print('')
rprint(type(parser))
rprint(parser)
# <class 'langchain_core.output_parsers.json.JsonOutputParser'>
# JsonOutputParser(pydantic_object=<class '__main__.Joke'>)


#################################################################################
### 2. streaming
### JsonOutputParser는 PydanticOutputParser와 다르게 부분 청크 스트리밍을 지원
print('2.', '-' * 50)
##################################################################################
for s in chain.stream({"query": joke_query}):
    print(s)
# 2. --------------------------------------------------
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


#################################################################################
### 3. Pydantic이 없는 JsonOutputParser 예시
print('3.', '-' * 50)
##################################################################################
joke_query = "Tell me a joke."

# parser = JsonOutputParser(pydantic_object=Joke)
parser = JsonOutputParser() ### Pydantic이 없는 JsonOutputParser

prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt | model | parser

rprint(chain.invoke({"query": joke_query}))
# 3. --------------------------------------------------
# {'response': "Sure! Here's a joke for you: Why couldn't the bicycle stand up by itself? Because it was two tired!"}

### parser.get_format_instructions() ###
print('')
rprint(parser.get_format_instructions())
# Return a JSON object.