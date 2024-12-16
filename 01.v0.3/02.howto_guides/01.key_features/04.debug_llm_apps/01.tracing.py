from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

#################################################################################
### 1. 도구 호출 시 콜백을 전파하지 않으면 astream_events()가 생성되지 않음
### RunnableLambdas나 @chain 데코레이터를 사용할 때, 콜백들은 자동으로 백그라운드에서 전파됨
print('1.', '-' * 50)
##################################################################################
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate

tools = [TavilySearchResults(max_results=1)]
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant.",
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

# Construct the Tools agent
agent = create_tool_calling_agent(llm, tools, prompt)

# Create an agent executor by passing in the agent and tools
agent_executor = AgentExecutor(agent=agent, tools=tools)
results = agent_executor.invoke(
    {"input": "Who directed the 2023 film Oppenheimer and what is their age in days?"}
)
rprint(results)
# 1. --------------------------------------------------
# {
#     'input': 'Who directed the 2023 film Oppenheimer and what is their age in days?',
#     'output': 'The 2023 film "Oppenheimer" was directed by Christopher Nolan.\n\nChristopher Nolan was born on July 30, 1970. To calculate his age in days as of today (October 12, 2023):\n\n1. 
# From July 30, 1970, to July 30, 2023, is 53 years.\n2. From July 30, 2023, to October 12, 2023, is 2 months and 12 days.\n\nNow, let\'s break that down into days:\n- 53 years = 53 * 365 = 
# 19,445 days (not accounting for leap years yet)\n- Leap years from 1970 to 2023: 1972, 1976, 1980, 1984, 1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016, 2020 = 13 leap years.\n\nTotal days from
# leap years = 13 days.\n\nTotal days from July 30, 1970, to July 30, 2023 = 19,445 + 13 = 19,458 days.\n\nNow, let\'s add the days from July 30, 2023, to October 12, 2023:\n- August has 31 days,
# hence 31 - 30 = 1 day in July (July 31).\n- August = 31 days.\n- September = 30 days.\n- October = 12 days.\n\nSo, from July 30 to October 12, we have:\n1 + 31 + 30 + 12 = 74 days.\n\nAdding 
# this to the previous total gives:\n19,458 + 74 = 19,532 days.\n\nTherefore, Christopher Nolan\'s age in days as of October 12, 2023, is **19,532 days**.'
# }

### LangSmith Tracing 확인 ###
# 1. LangSmith 로그인
# 2. 좌측 메뉴의 Tracing projects 클릭
# 3. LANGCHAIN_PRACTICE 클릭
# 4. AgentExecutor 클릭
# 5. 우측의 내용 확인