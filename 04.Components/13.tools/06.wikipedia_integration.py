# Wikipedia 검색을 실행하는 LangChain 도구
from langchain_community.tools import WikipediaQueryRun
# Wikipedia API와 상호작용하기 위한 래퍼 클래스
from langchain_community.utilities import WikipediaAPIWrapper

# WikipediaAPIWrapper의 인스턴스 - top_k_results=1: 검색 결과 중 상위 1개만 반환 / doc_content_chars_max=100: 각 문서의 내용을 최대 100자로 제한
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
# WikipediaQueryRun의 인스턴스 - api_wrapper 연결 / 쿼리를 실행하고 결과를 반환
tool = WikipediaQueryRun(api_wrapper=api_wrapper)

print(tool.invoke({"query": "langchain"}))
# Page: LangChain
# Summary: LangChain is a framework designed to simplify the creation of applications 

print('-'*30)
print(f"Name: {tool.name}")
# Name: wikipedia
print(f"Description: {tool.description}")
# Description: A wrapper around Wikipedia. Useful for when you need to answer general questions about people, places, companies, facts, historical events, or other subjects. Input should be a search query.
print(f"args schema: {tool.args}")
# args schema: {'query': {'title': 'Query', 'description': 'query to look up on wikipedia', 'type': 'string'}}
print(f"returns directly?: {tool.return_direct}")
# returns directly?: False