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
        ("system", "You are a helpful assistant."),
        ("human", "{input}"),
        # Placeholders fill up a **list** of messages
        ("placeholder", "{agent_scratchpad}"),
    ]
)


@tool
def magic_function(input: int) -> int:
    """Applies a magic function to an input."""
    return "Sorry there was an error, please try again."


tools = [magic_function]


### 1. LangChain
agent = create_tool_calling_agent(model, tools, prompt=prompt)
agent_executor = AgentExecutor(
    agent=agent, tools=tools, early_stopping_method="force", max_iterations=1
)

result = agent_executor.invoke({"input": query})
print("Output with early_stopping_method='force':")
print(result["output"])
# Output with early_stopping_method='force':
# Agent stopped due to max iterations.


### 2. LangGraph
print("-" * 30)
from langgraph.errors import GraphRecursionError
from langgraph.prebuilt import create_react_agent

RECURSION_LIMIT = 2 * 1 + 1

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
# content='what is the value of magic_function(3)?' id='86ad57fe-cd72-4127-b093-8836d7ca5473'
# content='' additional_kwargs={'tool_calls': [{'id': 'call_E6TSlhyq35hCU77WY7PARsiG', 'function': {'arguments': '{"input":3}', 'name': 'magic_function'}, 'type': 'function'}]} response_metadata={'token_usage': {'completion_tokens': 14, 'prompt_tokens': 55, 'total_tokens': 69}, 'model_name': 'gpt-4o-2024-05-13', 'system_fingerprint': 'fp_dd932ca5d1', 'finish_reason': 'tool_calls', 'logprobs': None} id='run-affcb73f-77d0-4a7e-a472-a69fc0aa9f88-0' tool_calls=[{'name': 'magic_function', 'args': {'input': 3}, 'id': 'call_E6TSlhyq35hCU77WY7PARsiG'}] usage_metadata={'input_tokens': 55, 'output_tokens': 14, 'total_tokens': 69}
# content='Sorry there was an error, please try again.' name='magic_function' id='f74618df-bb44-4a35-8b5e-1b0ba85030a5' tool_call_id='call_E6TSlhyq35hCU77WY7PARsiG'
# content='' additional_kwargs={'tool_calls': [{'id': 'call_NSTZhtZQYAwV4CpkbcVVIEEh', 'function': {'arguments': '{"input":3}', 'name': 'magic_function'}, 'type': 'function'}]} response_metadata={'token_usage': {'completion_tokens': 14, 'prompt_tokens': 87, 'total_tokens': 101}, 'model_name': 'gpt-4o-2024-05-13', 'system_fingerprint': 'fp_d33f7b429e', 'finish_reason': 'tool_calls', 'logprobs': None} id='run-c902ded0-1af3-4dbc-a848-df59c5a1976d-0' tool_calls=[{'name': 'magic_function', 'args': {'input': 3}, 'id': 'call_NSTZhtZQYAwV4CpkbcVVIEEh'}] usage_metadata={'input_tokens': 87, 'output_tokens': 14, 'total_tokens': 101}
# {'input': 'what is the value of magic_function(3)?', 'output': 'Agent stopped due to max iterations.'}    