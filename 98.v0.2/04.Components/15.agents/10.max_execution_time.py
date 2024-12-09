from dotenv import load_dotenv
load_dotenv()

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
import time


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
    time.sleep(2.5)
    return "Sorry, there was an error. Please try again."


tools = [magic_function]

agent = create_tool_calling_agent(model, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    max_execution_time=2,
    verbose=True,
)

print(agent_executor.invoke({"input": query}))
# > Entering new AgentExecutor chain...
# Invoking: `magic_function` with `{'input': '3'}`
# Sorry, there was an error. Please try again.
# > Finished chain.
# {'input': 'what is the value of magic_function(3)?', 'output': 'Agent stopped due to max iterations.'}


### 2. LangGraph
print('-'*30)
from langgraph.prebuilt import create_react_agent

app = create_react_agent(model, tools=tools)
# Set the max timeout for each step here
app.step_timeout = 2

try:
    for chunk in app.stream({"messages": [("human", query)]}):
        print(chunk)
        print("------")
# except TimeoutError:
except Exception as e:    
    print(f'Error: {e}')
    # print({"input": query, "output": "Agent stopped due to max iterations."})
### 'TimeoutError'가 아닌 다른 error가 발생함.
# Error: local variable 'fut' referenced before assignment    