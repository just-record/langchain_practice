from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

llm = ChatOpenAI(model="gpt-4o-mini")


# Define a new graph
workflow = StateGraph(state_schema=MessagesState)


# Define the function that calls the model
def call_model(state: MessagesState):
    response = llm.invoke(state["messages"])
    # Update message history with response:
    return {"messages": response}


# Define the (single) node in the graph
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# Add memory
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

##################################################################################
### 1. Example: message inputs
print('1.', '-' * 50)
##################################################################################
config = {"configurable": {"thread_id": "abc123"}}

query = "Hi! I'm Bob."

input_messages = [HumanMessage(query)]
output = app.invoke({"messages": input_messages}, config)
output["messages"][-1].pretty_print()  # output contains all messages in state
# 1. --------------------------------------------------
# ================================== Ai Message ==================================

# Hi Bob! How can I assist you today?


query = "What's my name?"

input_messages = [HumanMessage(query)]
output = app.invoke({"messages": input_messages}, config)
output["messages"][-1].pretty_print()
# ================================== Ai Message ==================================

# Your name is Bob! How can I help you today, Bob?


##################################################################################
### 2. Example: message inputs - thread_id 변경하기
print('2.', '-' * 50)
##################################################################################
query = "What's my name?"
config = {"configurable": {"thread_id": "abc234"}}

input_messages = [HumanMessage(query)]
output = app.invoke({"messages": input_messages}, config)
output["messages"][-1].pretty_print()
# 2. --------------------------------------------------
# ================================== Ai Message ==================================

# I'm sorry, but I don't know your name. You haven't shared it with me yet. If you'd like to tell me, feel free!
