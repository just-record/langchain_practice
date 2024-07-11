from dotenv import load_dotenv
load_dotenv()

### 1. LangChain
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

agent = create_tool_calling_agent(model, tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

for step in agent_executor.stream({"input": query}):
    print(f'step: {step}')
# step: {'actions': [ToolAgentAction(tool='magic_function', tool_input={'input': 3}, log="\nInvoking: `magic_function` with `{'input': 3}`\n\n\n", message_log=[AIMessageChunk(content='', additional_kwargs={'tool_calls': [{'index': 0, 'id': 'call_uwH8cpohlNqx3aTOIjeikfYq', 'function': {'arguments': '{"input":3}', 'name': 'magic_function'}, 'type': 'function'}]}, response_metadata={'finish_reason': 'tool_calls', 'model_name': 'gpt-4o-2024-05-13', 'system_fingerprint': 'fp_dd932ca5d1'}, id='run-15075462-d258-4fc0-994c-77364eca58f1', tool_calls=[{'name': 'magic_function', 'args': {'input': 3}, 'id': 'call_uwH8cpohlNqx3aTOIjeikfYq'}], tool_call_chunks=[{'name': 'magic_function', 'args': '{"input":3}', 'id': 'call_uwH8cpohlNqx3aTOIjeikfYq', 'index': 0}])], tool_call_id='call_uwH8cpohlNqx3aTOIjeikfYq')], 'messages': [AIMessageChunk(content='', additional_kwargs={'tool_calls': [{'index': 0, 'id': 'call_uwH8cpohlNqx3aTOIjeikfYq', 'function': {'arguments': '{"input":3}', 'name': 'magic_function'}, 'type': 'function'}]}, response_metadata={'finish_reason': 'tool_calls', 'model_name': 'gpt-4o-2024-05-13', 'system_fingerprint': 'fp_dd932ca5d1'}, id='run-15075462-d258-4fc0-994c-77364eca58f1', tool_calls=[{'name': 'magic_function', 'args': {'input': 3}, 'id': 'call_uwH8cpohlNqx3aTOIjeikfYq'}], tool_call_chunks=[{'name': 'magic_function', 'args': '{"input":3}', 'id': 'call_uwH8cpohlNqx3aTOIjeikfYq', 'index': 0}])]}
# step: {'steps': [AgentStep(action=ToolAgentAction(tool='magic_function', tool_input={'input': 3}, log="\nInvoking: `magic_function` with `{'input': 3}`\n\n\n", message_log=[AIMessageChunk(content='', additional_kwargs={'tool_calls': [{'index': 0, 'id': 'call_uwH8cpohlNqx3aTOIjeikfYq', 'function': {'arguments': '{"input":3}', 'name': 'magic_function'}, 'type': 'function'}]}, response_metadata={'finish_reason': 'tool_calls', 'model_name': 'gpt-4o-2024-05-13', 'system_fingerprint': 'fp_dd932ca5d1'}, id='run-15075462-d258-4fc0-994c-77364eca58f1', tool_calls=[{'name': 'magic_function', 'args': {'input': 3}, 'id': 'call_uwH8cpohlNqx3aTOIjeikfYq'}], tool_call_chunks=[{'name': 'magic_function', 'args': '{"input":3}', 'id': 'call_uwH8cpohlNqx3aTOIjeikfYq', 'index': 0}])], tool_call_id='call_uwH8cpohlNqx3aTOIjeikfYq'), observation=5)], 'messages': [FunctionMessage(content='5', name='magic_function')]}
# step: {'output': 'The value of `magic_function(3)` is 5.', 'messages': [AIMessage(content='The value of `magic_function(3)` is 5.')]}   


### 2. LangGraph
print('-'*30)
from langchain_core.messages import AnyMessage
from langgraph.prebuilt import create_react_agent

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        ("placeholder", "{messages}"),
    ]
)


def _modify_messages(messages: list[AnyMessage]):
    return prompt.invoke({"messages": messages}).to_messages()


app = create_react_agent(model, tools, messages_modifier=_modify_messages)


for step in app.stream({"messages": [("human", query)]}, stream_mode="updates"):
    print(f'step: {step}')
# step: {'agent': {'messages': [AIMessage(content='', additional_kwargs={'tool_calls': [{'id': 'call_gMLCuwTuMopyAKXz2QV4bxAE', 'function': {'arguments': '{"input":3}', 'name': 'magic_function'}, 'type': 'function'}]}, response_metadata={'token_usage': {'completion_tokens': 14, 'prompt_tokens': 61, 'total_tokens': 75}, 'model_name': 'gpt-4o-2024-05-13', 'system_fingerprint': 'fp_dd932ca5d1', 'finish_reason': 'tool_calls', 'logprobs': None}, id='run-5595332b-c17c-4cc2-8277-80d526bc7dbb-0', tool_calls=[{'name': 'magic_function', 'args': {'input': 3}, 'id': 'call_gMLCuwTuMopyAKXz2QV4bxAE'}], usage_metadata={'input_tokens': 61, 'output_tokens': 14, 'total_tokens': 75})]}}
# step: {'tools': {'messages': [ToolMessage(content='5', name='magic_function', tool_call_id='call_gMLCuwTuMopyAKXz2QV4bxAE')]}}
# step: {'agent': {'messages': [AIMessage(content='The value of `magic_function(3)` is 5.', response_metadata={'token_usage': {'completion_tokens': 14, 'prompt_tokens': 84, 'total_tokens': 98}, 'model_name': 'gpt-4o-2024-05-13', 'system_fingerprint': 'fp_d33f7b429e', 'finish_reason': 'stop', 'logprobs': None}, id='run-f383935d-f36f-45c7-9d9e-b4502c86e6e2-0', usage_metadata={'input_tokens': 84, 'output_tokens': 14, 'total_tokens': 98})]}}    
