from dotenv import load_dotenv
load_dotenv()

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        ("human", "{input}"),
        # Placeholders fill up a **list** of messages
        ("placeholder", "{agent_scratchpad}"),
    ]
)

magic_step_num = 1

@tool
def magic_function(input: int) -> int:
    """Applies a magic function to an input."""
    global magic_step_num
    print(f"Call number: {magic_step_num}")
    magic_step_num += 1
    return input + magic_step_num


tools = [magic_function]


### 1. LangChain
agent = create_tool_calling_agent(model, tools, prompt=prompt)

def trim_steps(steps: list):
    # Let's give the agent amnesia
    return []


agent_executor = AgentExecutor(
    agent=agent, tools=tools, trim_intermediate_steps=trim_steps
)

query = "Call the magic function 4 times in sequence with the value 3. You cannot call it multiple times at once."

for step in agent_executor.stream({"input": query}):
    pass
    # print(f'step: {step}')
# Call number: 1
# Call number: 2
# Call number: 3
# Call number: 4
# Call number: 5
# Call number: 6
# Call number: 7
# Call number: 8
# Call number: 9
# Call number: 10
# Call number: 11
# Call number: 12
# Call number: 13
# Call number: 14
# Call number: 15
# Stopping agent prematurely due to triggering stop condition    


### 2. LangGraph
print('-'*30)
from langchain_core.messages import AnyMessage
from langgraph.errors import GraphRecursionError
from langgraph.prebuilt import create_react_agent

magic_step_num = 1


@tool
def magic_function(input: int) -> int:
    """Applies a magic function to an input."""
    global magic_step_num
    print(f"Call number: {magic_step_num}")
    magic_step_num += 1
    return input + magic_step_num


tools = [magic_function]


def _modify_messages(messages: list[AnyMessage]):
    # Give the agent amnesia, only keeping the original user query
    return [("system", "You are a helpful assistant"), messages[0]]


app = create_react_agent(model, tools, messages_modifier=_modify_messages)

try:
    for step in app.stream({"messages": [("human", query)]}, stream_mode="updates"):
        pass
except GraphRecursionError as e:
    print("Stopping agent prematurely due to triggering stop condition")
# Call number: 1
# Call number: 2
# Call number: 3
# Call number: 4
# Call number: 5
# Call number: 6
# Call number: 7
# Call number: 8
# Call number: 9
# Call number: 10
# Call number: 11
# Call number: 12
# Stopping agent prematurely due to triggering stop condition    
