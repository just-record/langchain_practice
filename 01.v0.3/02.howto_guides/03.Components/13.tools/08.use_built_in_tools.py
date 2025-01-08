# pip install -qU langchain-community wikipedia
# wikipedia: Python에서 Wikipedia API를 쉽게 사용할 수 있게 해주는 라이브러리

from rich import print as rprint
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper


#################################################################################
### 1. Tools - WikipediaAPIWrapper, WikipediaQueryRun 예시
print('1.', '-' * 50)
################################################################################## 
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
tool = WikipediaQueryRun(api_wrapper=api_wrapper)

rprint(tool.invoke({"query": "langchain"}))
# 1. --------------------------------------------------
# Page: LangChain
# Summary: LangChain is a software framework that helps facilitate the integration of 

print(' ')
rprint(f"Name: {tool.name}")
rprint(f"Description: {tool.description}")
rprint(f"args schema: {tool.args}")
rprint(f"returns directly?: {tool.return_direct}")
# Name: wikipedia
# Description: A wrapper around Wikipedia. Useful for when you need to answer general questions about people, places, companies, facts, historical events, or other subjects. Input should be a search query.
# args schema: {'query': {'description': 'query to look up on wikipedia', 'title': 'Query', 'type': 'string'}}
# returns directly?: False


#################################################################################
### 2. Customizing Default Tools
### 내장된 이름, 설명, 그리고 인자들의 JSON 스키마를 수정할 수 있습니다.
### 인자들의 JSON 스키마를 정의할 때, 함수와 동일한 입력값을 유지하는 것이 중요하므로 이를 변경해서는 안 됩니다. 
### 하지만 각 입력값에 대한 사용자 정의 설명을 쉽게 추가할 수 있습니다.
print('2.', '-' * 50)
################################################################################## 
from pydantic import BaseModel, Field


class WikiInputs(BaseModel):
    """Inputs to the wikipedia tool."""

    query: str = Field(
        description="query to look up in Wikipedia, should be 3 or less words"
    )


tool = WikipediaQueryRun(
    name="wiki-tool",
    description="look up things in wikipedia",
    args_schema=WikiInputs,
    api_wrapper=api_wrapper,
    return_direct=True,
)

print(tool.run("langchain"))
# 2. --------------------------------------------------
# Page: LangChain
# Summary: LangChain is a software framework that helps facilitate the integration of 

print(' ')
rprint(f"Name: {tool.name}")
rprint(f"Description: {tool.description}")
rprint(f"args schema: {tool.args}")
rprint(f"returns directly?: {tool.return_direct}")
# Name: wiki-tool
# Description: look up things in wikipedia
# args schema: {'query': {'description': 'query to look up in Wikipedia, should be 3 or less words', 'title': 'Query', 'type': 'string'}}
# returns directly?: True


#################################################################################
### 3. How to use built-in toolkits
### 툴킷은 특정 작업을 위해 함께 사용되도록 설계된 도구들의 모음입니다. 
### 툴킷에는 편리한 로딩 방법이 있습니다.
### 모든 툴킷은 도구 목록을 반환하는 get_tools 메서드를 제공합니다.
################################################################################## 
### Initialize a toolkit
# toolkit = ExampleTookit(...)

### Get list of tools
# tools = toolkit.get_tools()