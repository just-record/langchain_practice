# 이 출력 파서는 다른 출력 파서를 감싸고 있으며, 첫 번째 파서가 실패할 경우 오류를 수정하기 위해 다른 LLM을 호출합니다.
# 하지만 단순히 오류를 발생시키는 것 외에도 다른 작업을 수행할 수 있습니다. 구체적으로, 잘못 포맷된 출력과 포맷 지침을 모델에 전달하여 수정을 요청할 수 있습니다.

from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint


#################################################################################
### 1. Outpur parser를 사용 할 때 오류 발생 
### 출력에 문제가 있는 경우: 형식이 틀렸거나 내용이 부족한 경우
print('1.', '-' * 50)
##################################################################################
from typing import List

from langchain_core.exceptions import OutputParserException
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


class Actor(BaseModel):
    name: str = Field(description="name of an actor")
    film_names: List[str] = Field(description="list of names of films they starred in")


actor_query = "Generate the filmography for a random actor."

parser = PydanticOutputParser(pydantic_object=Actor)

### 출력이 잘못된 경우를 설정 ###
misformatted = "{'name': 'Tom Hanks', 'film_names': ['Forrest Gump']}"

try:
    parser.parse(misformatted)
except OutputParserException as e:
    print(e)
# 1. --------------------------------------------------
# Invalid json output: {'name': 'Tom Hanks', 'film_names': ['Forrest Gump']}
# For troubleshooting, visit: https://python.langchain.com/docs/troubleshooting/errors/OUTPUT_PARSING_FAILURE     


#################################################################################
### 2. 출력 오류 수정하기 - 출력문으로 수정
### 다른 출력 파서를 인자로 받으며, 형식 오류를 수정하기 위해 LLM도 함께 사용
print('2.', '-' * 50)
##################################################################################
from langchain.output_parsers import OutputFixingParser

new_parser = OutputFixingParser.from_llm(parser=parser, llm=ChatOpenAI())
rprint(new_parser.parse(misformatted))
# 2. --------------------------------------------------
# Actor(name='Tom Hanks', film_names=['Forrest Gump'])