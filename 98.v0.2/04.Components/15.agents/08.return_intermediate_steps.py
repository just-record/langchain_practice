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
    return input + 2


tools = [magic_function]

### 1. LangChain
agent = create_tool_calling_agent(model, tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, return_intermediate_steps=True)
result = agent_executor.invoke({"input": query})
print(result["intermediate_steps"])
# [(ToolAgentAction(tool='magic_function', tool_input={'input': 3}, log="\nInvoking: `magic_function` with `{'input': 3}`\n\n\n", message_log=[AIMessageChunk(content='', additional_kwargs={'tool_calls': [{'index': 0, 'id': 'call_C8uSC76FVxWTxnsjotwtI5av', 'function': {'arguments': '{"input":3}', 'name': 'magic_function'}, 'type': 'function'}]}, response_metadata={'finish_reason': 'tool_calls', 'model_name': 'gpt-4o-2024-05-13', 'system_fingerprint': 'fp_dd932ca5d1'}, id='run-5c83d73d-a933-4ef6-a450-2ff4dfe088bb', tool_calls=[{'name': 'magic_function', 'args': {'input': 3}, 'id': 'call_C8uSC76FVxWTxnsjotwtI5av'}], tool_call_chunks=[{'name': 'magic_function', 'args': '{"input":3}', 'id': 'call_C8uSC76FVxWTxnsjotwtI5av', 'index': 0}])], tool_call_id='call_C8uSC76FVxWTxnsjotwtI5av'), 5)]


### 2. LangGraph
print('-'*30)
from langgraph.prebuilt import create_react_agent

app = create_react_agent(model, tools=tools)

messages = app.invoke({"messages": [("human", query)]})

print(messages)
# {'messages': [HumanMessage(content='what is the value of magic_function(3)?', id='ab6747ce-6daf-4a53-a3b9-bf9a3433f82c'), AIMessage(content='', additional_kwargs={'tool_calls': [{'id': 'call_ddvKC1nRMCi2y14xT45lRCG5', 'function': {'arguments': '{"input":3}', 'name': 'magic_function'}, 'type': 'function'}]}, response_metadata={'token_usage': {'completion_tokens': 14, 'prompt_tokens': 55, 'total_tokens': 69}, 'model_name': 'gpt-4o-2024-05-13', 'system_fingerprint': 'fp_dd932ca5d1', 'finish_reason': 'tool_calls', 'logprobs': None}, id='run-df161573-c518-40a5-8ba1-edac5830a881-0', tool_calls=[{'name': 'magic_function', 'args': {'input': 3}, 'id': 'call_ddvKC1nRMCi2y14xT45lRCG5'}], usage_metadata={'input_tokens': 55, 'output_tokens': 14, 'total_tokens': 69}), ToolMessage(content='5', name='magic_function', id='86d5c4e9-7b3a-4831-8f62-a2ca8a9e5199', tool_call_id='call_ddvKC1nRMCi2y14xT45lRCG5'), AIMessage(content='The value of `magic_function(3)` is 5.', response_metadata={'token_usage': {'completion_tokens': 14, 'prompt_tokens': 78, 'total_tokens': 92}, 'model_name': 'gpt-4o-2024-05-13', 'system_fingerprint': 'fp_d33f7b429e', 'finish_reason': 'stop', 'logprobs': None}, id='run-706a0437-ca39-4dce-85d0-a832518db67a-0', usage_metadata={'input_tokens': 78, 'output_tokens': 14, 'total_tokens': 92})]}