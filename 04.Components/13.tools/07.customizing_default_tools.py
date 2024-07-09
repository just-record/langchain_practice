from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.pydantic_v1 import BaseModel, Field

api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)

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
# Page: LangChain
# Summary: LangChain is a framework designed to simplify the creation of applications 

print('-'*30)
print(f"Name: {tool.name}")
# Name: wiki-tool
print(f"Description: {tool.description}")
# Description: look up things in wikipedia
print(f"args schema: {tool.args}")
# args schema: {'query': {'title': 'Query', 'description': 'query to look up in Wikipedia, should be 3 or less words', 'type': 'string'}}
print(f"returns directly?: {tool.return_direct}")
# returns directly?: False