from dotenv import load_dotenv
load_dotenv()

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor


model = ChatOpenAI(model="gpt-4o")

@tool
def magic_function(input: int) -> int:
    """Applies a magic function to an input."""
    return input + 2


tools = [magic_function]

query = "what is the value of magic_function(3)?"

### 1. LangChain AgentExcutor - a prompt with a placeholder for the agent's scratchpad
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Respond only in Spanish."),
        ("human", "{input}"),
        # Placeholders fill up a **list** of messages
        ("placeholder", "{agent_scratchpad}"),
    ]
)

agent = create_tool_calling_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

print(agent_executor.invoke({"input": query}))
# {'input': 'what is the value of magic_function(3)?', 'output': 'El valor de `magic_function(3)` es 5.'}


### 2. create_react_agent - LangGraph
print('-'*30)
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent

system_message = "You are a helpful assistant. Respond only in Spanish."
# This could also be a SystemMessage object
# system_message = SystemMessage(content="You are a helpful assistant. Respond only in Spanish.")

app = create_react_agent(model, tools, messages_modifier=system_message)

messages = app.invoke({"messages": [("user", query)]})
for i, message in enumerate(messages["messages"]):
    print(f'{i+1}번째: {message}')
# 1번째: content='what is the value of magic_function(3)?' id='5b08dfa9-4a8e-40a7-a6cb-b5cc3bddceb1'
# 2번째: content='' additional_kwargs={'tool_calls': [{'id': 'call_EVZLonGdfElCEDeAtomlsuaZ', 'function': {'arguments': '{"input":3}', 'name': 'magic_function'}, 'type': 'function'}]} response_metadata={'token_usage': {'completion_tokens': 14, 'prompt_tokens': 66, 'total_tokens': 80}, 'model_name': 'gpt-4o-2024-05-13', 'system_fingerprint': 'fp_d33f7b429e', 'finish_reason': 'tool_calls', 'logprobs': None} id='run-551e00cf-d007-40ee-a967-34f1d1255792-0' tool_calls=[{'name': 'magic_function', 'args': {'input': 3}, 'id': 'call_EVZLonGdfElCEDeAtomlsuaZ'}] usage_metadata={'input_tokens': 66, 'output_tokens': 14, 'total_tokens': 80}
# 3번째: content='5' name='magic_function' id='3d906439-7719-43d5-90e8-a95a43852d2c' tool_call_id='call_EVZLonGdfElCEDeAtomlsuaZ'
# 4번째: content='El valor de `magic_function(3)` es 5.' response_metadata={'token_usage': {'completion_tokens': 14, 'prompt_tokens': 89, 'total_tokens': 103}, 'model_name': 'gpt-4o-2024-05-13', 'system_fingerprint': 'fp_d33f7b429e', 'finish_reason': 'stop', 'logprobs': None} id='run-c2b3efd9-6865-4b89-a18a-909933e5787e-0' usage_metadata={'input_tokens': 89, 'output_tokens': 14, 'total_tokens': 103}    