from dotenv import load_dotenv
load_dotenv()

from typing import List

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI

class Actor(BaseModel):
    name: str = Field(description="name of an actor")
    film_names: List[str] = Field(description="list of names of films they starred in")


actor_query = "Generate the filmography for a random actor."

parser = PydanticOutputParser(pydantic_object=Actor)

misformatted = "{'name': 'Tom Hanks', 'film_names': ['Forrest Gump']}"

### 1. 잘못 된 결과값으로 인해 parsing시 에러 발생
try:
    parser.parse(misformatted)
except Exception as e:
    print(f'Error: {e}')
# Error: Invalid json output: {'name': 'Tom Hanks', 'film_names': ['Forrest Gump']}    


### 2. OutputFixingParser를 사용하여 오류를 수정
### Error가 발생 한다. 시간을 두고 원인을 찾아야 할 듯
### <https://wikidocs.net/233793>에서도 같은 문제가 발생함
print('-'*30)
from langchain.output_parsers import OutputFixingParser

new_parser = OutputFixingParser.from_llm(parser=parser, llm=ChatOpenAI())

print(new_parser.parse(misformatted))
# KeyError: "Input to PromptTemplate is missing variables {'completion'}.  Expected: ['completion', 'error', 'instructions'] Received: ['instructions', 'input', 'error']"
