# 콜백 컨텍스트 매니저들이 있어서 여러 호출에 걸쳐 토큰 사용량을 추적
# OpenAI API와 Bedrock Anthropic API에서만 구현

from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from langchain_openai import ChatOpenAI


from langchain_community.callbacks.manager import get_openai_callback

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    stream_usage=True,
)

#################################################################################
### 1. Using callbacks - openai
print('1.', '-' * 50)
##################################################################################
with get_openai_callback() as cb:
    result = llm.invoke("Tell me a joke")
    rprint(cb)
# 1. --------------------------------------------------
# Tokens Used: 30
#         Prompt Tokens: 11
#         Completion Tokens: 19
# Successful Requests: 1
# Total Cost (USD): $1.3049999999999999e-05    


#################################################################################
### 2. multiple calls - 순차적 호출 - openai
print('2.', '-' * 50)
##################################################################################
with get_openai_callback() as cb:
    result = llm.invoke("Tell me a joke")
    result2 = llm.invoke("Tell me a joke")
    # rprint(cb.total_tokens)
    rprint(cb)
# 2. --------------------------------------------------
# Tokens Used: 60
#         Prompt Tokens: 22
#         Completion Tokens: 38
# Successful Requests: 2
# Total Cost (USD): $2.6099999999999997e-05    


#################################################################################
### 3. multiple calls - 스트리밍 - openai
print('3.', '-' * 50)
##################################################################################
with get_openai_callback() as cb:
    for chunk in llm.stream("Tell me a joke"):
        pass
    rprint(cb)
# 3. --------------------------------------------------
# Tokens Used: 28
#         Prompt Tokens: 11
#         Completion Tokens: 17
# Successful Requests: 1
# Total Cost (USD): $1.185e-05    
    
    
#################################################################################
### 4. multiple calls - Agent - openai
print('4.', '-' * 50)
##################################################################################    
# pip install -qU langchain langchain-aws wikipedia
from langchain.agents import AgentExecutor, create_tool_calling_agent, load_tools
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You're a helpful assistant"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)
tools = load_tools(["wikipedia"])
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


with get_openai_callback() as cb:
    response = agent_executor.invoke(
        {
            "input": "What's a hummingbird's scientific name and what's the fastest bird species?"
        }
    )
    print(f"Total Tokens: {cb.total_tokens}")
    print(f"Prompt Tokens: {cb.prompt_tokens}")
    print(f"Completion Tokens: {cb.completion_tokens}")
    print(f"Total Cost (USD): ${cb.total_cost}")
# Total Tokens: 1826
# Prompt Tokens: 1682
# Completion Tokens: 144
# Total Cost (USD): $0.0003387    


#################################################################################
### 5. multiple calls - 순차적 호출 - anthropic
### 실습 생략 - aws의 API KEY가 필요함
### pip install -qU langchain langchain-aws
# print('5.', '-' * 50)
##################################################################################
# from langchain_aws import ChatBedrock
# from langchain_community.callbacks.manager import get_bedrock_anthropic_callback

# llm = ChatBedrock(model_id="anthropic.claude-v2")

# with get_bedrock_anthropic_callback() as cb:
#     result = llm.invoke("Tell me a joke")
#     result2 = llm.invoke("Tell me a joke")
#     print(cb)
### 공식 사이트의 결과 값
# Tokens Used: 96
# 	Prompt Tokens: 26
# 	Completion Tokens: 70
# Successful Requests: 2
# Total Cost (USD): $0.001888
