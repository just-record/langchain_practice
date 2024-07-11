from dotenv import load_dotenv
load_dotenv()

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o")


@tool
def magic_function(input: int) -> int:
    """Applies a magic function to an input."""
    return input + 2


tools = [magic_function]


query = "what is the value of magic_function(3)?"


### 1. LangChain AgentExcutor - a prompt with a placeholder for the agent's scratchpad
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant"),
        ("human", "{input}"),
        # Placeholders fill up a **list** of messages
        ("placeholder", "{agent_scratchpad}"),
    ]
)


agent = create_tool_calling_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

print(agent_executor.invoke({"input": query}))
# {'input': 'what is the value of magic_function(3)?', 'output': 'The value of `magic_function(3)` is 5.'}


### 2. create_react_agent - LangGraph
# https://langchain-ai.github.io/langgraph/reference/prebuilt/#create_react_agent
print('-'*30)
from langgraph.prebuilt import create_react_agent

app = create_react_agent(model, tools)


messages = app.invoke({"messages": [("human", query)]})
{
    "input": query,
    "output": messages["messages"][-1].content,
}
for i, message in enumerate(messages["messages"]):
    print(f'{i+1}번째: {message}')
# 1번째: content='what is the value of magic_function(3)?' id='778d09b0-e7db-4cd9-8aef-fd2b225f58dd'
# 2번째: content='' additional_kwargs={'tool_calls': [{'id': 'call_j7YS4IEiAMNIO9K2fFDEpQPT', 'function': {'arguments': '{"input":3}', 'name': 'magic_function'}, 'type': 'function'}]} response_metadata={'token_usage': {'completion_tokens': 14, 'prompt_tokens': 55, 'total_tokens': 69}, 'model_name': 'gpt-4o-2024-05-13', 'system_fingerprint': 'fp_298125635f', 'finish_reason': 'tool_calls', 'logprobs': None} id='run-d6e50903-d115-4924-a538-39e308288390-0' tool_calls=[{'name': 'magic_function', 'args': {'input': 3}, 'id': 'call_j7YS4IEiAMNIO9K2fFDEpQPT'}] usage_metadata={'input_tokens': 55, 'output_tokens': 14, 'total_tokens': 69}
# 3번째: content='5' name='magic_function' id='e9976b80-8c28-4df3-be21-4bc6a6c21bd7' tool_call_id='call_j7YS4IEiAMNIO9K2fFDEpQPT'
# 4번째: content='The value of `magic_function(3)` is 5.' response_metadata={'token_usage': {'completion_tokens': 14, 'prompt_tokens': 78, 'total_tokens': 92}, 'model_name': 'gpt-4o-2024-05-13', 'system_fingerprint': 'fp_298125635f', 'finish_reason': 'stop', 'logprobs': None} id='run-2a6308b3-6709-41c8-8a3f-edacfcbc6018-0' usage_metadata={'input_tokens': 78, 'output_tokens': 14, 'total_tokens': 92}   

### 3. create_react_agent - chat history
print('-'*30)
message_history = messages["messages"]

new_query = "Pardon?"

messages = app.invoke({"messages": message_history + [("human", new_query)]})
{
    "input": new_query,
    "output": messages["messages"][-1].content,
}    
for i, message in enumerate(messages["messages"]):
    print(f'{i+1}번째: {message}')
# 1번째: content='what is the value of magic_function(3)?' id='778d09b0-e7db-4cd9-8aef-fd2b225f58dd'
# 2번째: content='' additional_kwargs={'tool_calls': [{'id': 'call_j7YS4IEiAMNIO9K2fFDEpQPT', 'function': {'arguments': '{"input":3}', 'name': 'magic_function'}, 'type': 'function'}]} response_metadata={'token_usage': {'completion_tokens': 14, 'prompt_tokens': 55, 'total_tokens': 69}, 'model_name': 'gpt-4o-2024-05-13', 'system_fingerprint': 'fp_298125635f', 'finish_reason': 'tool_calls', 'logprobs': None} id='run-d6e50903-d115-4924-a538-39e308288390-0' tool_calls=[{'name': 'magic_function', 'args': {'input': 3}, 'id': 'call_j7YS4IEiAMNIO9K2fFDEpQPT'}] usage_metadata={'input_tokens': 55, 'output_tokens': 14, 'total_tokens': 69}
# 3번째: content='5' name='magic_function' id='e9976b80-8c28-4df3-be21-4bc6a6c21bd7' tool_call_id='call_j7YS4IEiAMNIO9K2fFDEpQPT'
# 4번째: content='The value of `magic_function(3)` is 5.' response_metadata={'token_usage': {'completion_tokens': 14, 'prompt_tokens': 78, 'total_tokens': 92}, 'model_name': 'gpt-4o-2024-05-13', 'system_fingerprint': 'fp_298125635f', 'finish_reason': 'stop', 'logprobs': None} id='run-2a6308b3-6709-41c8-8a3f-edacfcbc6018-0' usage_metadata={'input_tokens': 78, 'output_tokens': 14, 'total_tokens': 92}
# 5번째: content='Pardon?' id='03eaec2b-fa9e-4670-a59f-9e084c2de96f'
# 6번째: content='The value returned by `magic_function(3)` is 5.' response_metadata={'token_usage': {'completion_tokens': 15, 'prompt_tokens': 102, 'total_tokens': 117}, 'model_name': 'gpt-4o-2024-05-13', 'system_fingerprint': 'fp_d33f7b429e', 'finish_reason': 'stop', 'logprobs': None} id='run-d0c2b685-398f-4619-8bb6-802cb57da5fa-0' usage_metadata={'input_tokens': 102, 'output_tokens': 15, 'total_tokens': 117}  