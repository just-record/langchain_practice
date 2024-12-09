from dotenv import load_dotenv
load_dotenv()

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o")

query = "what is the value of magic_function(3)?"

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Respond only in Spanish."),
        ("human", "{input}"),
        # Placeholders fill up a **list** of messages
        ("placeholder", "{agent_scratchpad}"),
    ]
)


@tool
def magic_function(input: str) -> str:
    """Applies a magic function to an input."""
    print(f"===Invoking===: `magic_function` with `{input}`")
    return "Sorry, there was an error. Please try again."


tools = [magic_function]

### 1. LangChain
agent = create_tool_calling_agent(model, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=3,
)

print(agent_executor.invoke({"input": query}))
# > Entering new AgentExecutor chain...
# Invoking: `magic_function` with `{'input': '3'}`
# ===Invoking===: `magic_function` with `3`
# Sorry, there was an error. Please try again.Hubo un error al intentar calcular el valor. ¿Podrías intentar nuevamente o proporcionar más información?
# > Finished chain.
# {'input': 'what is the value of magic_function(3)?', 'output': 'Hubo un error al intentar calcular el valor. ¿Podrías intentar nuevamente o proporcionar más información?'}
### 음~~~ 실행이 한 번 밖에 안 되네.


### 2. LangGraph
print('-'*30)
from langgraph.errors import GraphRecursionError
from langgraph.prebuilt import create_react_agent

RECURSION_LIMIT = 2 * 3 + 1

app = create_react_agent(model, tools=tools)

try:
    for chunk in app.stream(
        {"messages": [("human", query)]},
        {"recursion_limit": RECURSION_LIMIT},
        stream_mode="values",
    ):
        print(chunk["messages"][-1])
except GraphRecursionError:
    print({"input": query, "output": "Agent stopped due to max iterations."})
# content='what is the value of magic_function(3)?' id='fed55af3-f910-4fc0-b921-ae53eb1b65ca'
# content='' additional_kwargs={'tool_calls': [{'id': 'call_2ikFSSc6Uw2k8Ase65b9vP5B', 'function': {'arguments': '{"input":"3"}', 'name': 'magic_function'}, 'type': 'function'}]} response_metadata={'token_usage': {'completion_tokens': 14, 'prompt_tokens': 55, 'total_tokens': 69}, 'model_name': 'gpt-4o-2024-05-13', 'system_fingerprint': 'fp_dd932ca5d1', 'finish_reason': 'tool_calls', 'logprobs': None} id='run-8c70bdb5-b2ea-4c41-9515-d9dfddcfbca6-0' tool_calls=[{'name': 'magic_function', 'args': {'input': '3'}, 'id': 'call_2ikFSSc6Uw2k8Ase65b9vP5B'}] usage_metadata={'input_tokens': 55, 'output_tokens': 14, 'total_tokens': 69}
# ===Invoking===: `magic_function` with `3`
# content='Sorry, there was an error. Please try again.' name='magic_function' id='561ab798-d11e-4b55-bad0-35142e61b68e' tool_call_id='call_2ikFSSc6Uw2k8Ase65b9vP5B'
# content="It looks like there was an issue with calculating the value of `magic_function(3)`. Let's try that again.\n\nWhat is the value of `magic_function(3)`?" additional_kwargs={'tool_calls': [{'id': 'call_2wFMpBVLhuvEPNY5MpT8hNRg', 'function': {'arguments': '{"input":"3"}', 'name': 'magic_function'}, 'type': 'function'}]} response_metadata={'token_usage': {'completion_tokens': 51, 'prompt_tokens': 88, 'total_tokens': 139}, 'model_name': 'gpt-4o-2024-05-13', 'system_fingerprint': 'fp_d33f7b429e', 'finish_reason': 'tool_calls', 'logprobs': None} id='run-723ef24e-0ebc-405f-8d0a-37e0ce8eafc6-0' tool_calls=[{'name': 'magic_function', 'args': {'input': '3'}, 'id': 'call_2wFMpBVLhuvEPNY5MpT8hNRg'}] usage_metadata={'input_tokens': 88, 'output_tokens': 51, 'total_tokens': 139}
# ===Invoking===: `magic_function` with `3`
# content='Sorry, there was an error. Please try again.' name='magic_function' id='7873d73a-d2d7-454a-beba-984f9d12c285' tool_call_id='call_2wFMpBVLhuvEPNY5MpT8hNRg'
# content="It seems there is still an issue with calculating `magic_function(3)`. Let's try a different approach.\n\nWhat is the value of `magic_function(three)`?" additional_kwargs={'tool_calls': [{'id': 'call_7nkRDjNt9zFMT1M0Nj3LQSqj', 'function': {'arguments': '{"input":"three"}', 'name': 'magic_function'}, 'type': 'function'}]} response_metadata={'token_usage': {'completion_tokens': 49, 'prompt_tokens': 161, 'total_tokens': 210}, 'model_name': 'gpt-4o-2024-05-13', 'system_fingerprint': 'fp_d33f7b429e', 'finish_reason': 'tool_calls', 'logprobs': None} id='run-6eff38f4-4000-43f2-89bc-fd1b25cf94d3-0' tool_calls=[{'name': 'magic_function', 'args': {'input': 'three'}, 'id': 'call_7nkRDjNt9zFMT1M0Nj3LQSqj'}] usage_metadata={'input_tokens': 161, 'output_tokens': 49, 'total_tokens': 210}
# ===Invoking===: `magic_function` with `three`
# content='Sorry, there was an error. Please try again.' name='magic_function' id='a79a4150-2987-486d-8c93-18fc92a417fb' tool_call_id='call_7nkRDjNt9zFMT1M0Nj3LQSqj'
# content='It appears that the function is consistently encountering an issue. Unfortunately, I am unable to determine the value of `magic_function(3)` at this moment. If you have any other questions or need assistance with something else, please let me know!' response_metadata={'token_usage': {'completion_tokens': 50, 'prompt_tokens': 232, 'total_tokens': 282}, 'model_name': 'gpt-4o-2024-05-13', 'system_fingerprint': 'fp_dd932ca5d1', 'finish_reason': 'stop', 'logprobs': None} id='run-2938d6a2-a750-4045-b94c-37128123a860-0' usage_metadata={'input_tokens': 232, 'output_tokens': 50, 'total_tokens': 282}
# {'input': 'what is the value of magic_function(3)?', 'output': 'Agent stopped due to max iterations.'}    
### 3번 실행
