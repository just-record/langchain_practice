from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_community.callbacks.manager import get_openai_callback

llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)

### 1. 기본 사용법
with get_openai_callback() as cb:
    result = llm.invoke("Tell me a joke")
    print(cb)
# Tokens Used: 27
#         Prompt Tokens: 11
#         Completion Tokens: 16
# Successful Requests: 1
# Total Cost (USD): $2.95e-05    


### 2. multiple calls
print('-'*30)
with get_openai_callback() as cb:
    result = llm.invoke("Tell me a joke")
    result2 = llm.invoke("Tell me a joke")
    # print(cb.total_tokens)
    print(cb)
# Tokens Used: 54
#         Prompt Tokens: 22
#         Completion Tokens: 32
# Successful Requests: 2
# Total Cost (USD): $5.9e-05


### 3. streaming
print('-'*30)
with get_openai_callback() as cb:
    for chunk in llm.stream("Tell me a joke", stream_options={"include_usage": True}):
        pass
    print(cb)
# Tokens Used: 27
#         Prompt Tokens: 11
#         Completion Tokens: 16
# Successful Requests: 1
# Total Cost (USD): $0.0    


### 4. multiple steps
print('-'*30)
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
agent_executor = AgentExecutor(
    agent=agent, tools=tools, verbose=True, stream_runnable=False
)

with get_openai_callback() as cb:
    response = agent_executor.invoke(
        {
            "input": "What's a hummingbird's scientific name and what's the fastest bird species?"
        }
    )
    print(cb)
    # print(f"Total Tokens: {cb.total_tokens}")
    # print(f"Prompt Tokens: {cb.prompt_tokens}")
    # print(f"Completion Tokens: {cb.completion_tokens}")
    # print(f"Total Cost (USD): ${cb.total_cost}")
# Tokens Used: 1580
#         Prompt Tokens: 1480
#         Completion Tokens: 100
# Successful Requests: 2
# Total Cost (USD): $0.00089    


### 5. Bedrock Anthropic
### Anthropic의 token 사용량 체크 - Anthropic API 인증을 하지 않아 생략
# print('-'*30)
# from langchain_aws import ChatBedrock
# from langchain_community.callbacks.manager import get_bedrock_anthropic_callback

# llm = ChatBedrock(model_id="anthropic.claude-v2")

# with get_bedrock_anthropic_callback() as cb:
#     result = llm.invoke("Tell me a joke")
#     result2 = llm.invoke("Tell me a joke")
#     print(cb)