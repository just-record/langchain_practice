from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")


#################################################################################
### 1. 채팅 모델의 응답 형식은 제공업체에 따라 다를 수 있습니다.
### OpenAI의 채팅 모델은 일반적인 문자열 입력에 대해 문자열 형식의 내용을 반환
print('1.', '-' * 50)
##################################################################################
response = llm.invoke("Hello")
rprint(response.content)
# 1. --------------------------------------------------
# Hello! How can I assist you today?


#################################################################################
### 2. tool call이 생성될 때
### Antropic: 모델의 추론 과정을 전달하는 콘텐츠 블록으로 구성
### OpenAI: 빈 값
### tool_calls는 추가 됨
print('2.', '-' * 50)
##################################################################################

from langchain_core.tools import tool


@tool
def get_weather(location: str) -> str:
    """Get the weather from a location."""

    return "Sunny."


llm_with_tools = llm.bind_tools([get_weather])

response = llm_with_tools.invoke("What's the weather in San Francisco, CA?")
rprint(response)
# 2. --------------------------------------------------
### OpenAI
#

### Antropic
# {'text': "I'll help you get the current weather for San Francisco, CA. Let me retrieve that information for you.", 'type': 'text'},
# {'id': 'toolu_011TB8wjWXBLLa9mjmD4924Q', 'input': {'location': 'San Francisco, CA'}, 'name': 'get_weather', 'type': 'tool_use'}


#################################################################################
### 3. 메시지 객체의 형식에 관계없이 텍스트를 자동으로 파싱 - StrOutputParser
print('3.', '-' * 50)
##################################################################################
from langchain_core.output_parsers import StrOutputParser

# chain = llm_with_tools | StrOutputParser()
chain = llm | StrOutputParser()
response = chain.invoke("What's the weather in San Francisco, CA?")
rprint(response)
# 3. --------------------------------------------------
# I don't have real-time weather data. To get the current weather in San Francisco, CA, I recommend checking a reliable weather website or app.


#################################################################################
### 4. 스트리밍 사용
print('4.', '-' * 50)
##################################################################################
for chunk in chain.stream("What's the weather in San Francisco, CA?"):
    print(chunk, end="|")
# 4. --------------------------------------------------
# |I| can't| provide| real|-time| weather| information|.| For| the| latest| weather| updates| in| San| Francisco|,| CA|,| I| recommend| checking| a| reliable| weather| website| or| app|.||    