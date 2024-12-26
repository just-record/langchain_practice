from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

from typing import Sequence

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import Annotated, TypedDict

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


llm = ChatOpenAI(model="gpt-4o-mini")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Answer in {language}."),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

runnable = prompt | llm

class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    language: str


workflow = StateGraph(state_schema=State)


def call_model(state: State):
    response = runnable.invoke(state)
    # Update message history with response:
    return {"messages": [response]}


workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)


config = {"configurable": {"thread_id": "abc345"}}

input_dict = {
    "messages": [HumanMessage("Hi, I'm Bob.")],
    "language": "Spanish",
}
output = app.invoke(input_dict, config)
output["messages"][-1].pretty_print()


##################################################################################
### 1. Message history
print('1.', '-' * 50)
##################################################################################
state = app.get_state(config).values

print(f'Language: {state["language"]}')
for message in state["messages"]:
    message.pretty_print() 
# 1. --------------------------------------------------
# Language: Spanish
# ================================ Human Message =================================

# Hi, I'm Bob.
# ================================== Ai Message ==================================

# ¡Hola, Bob! ¿Cómo puedo ayudarte hoy?    


##################################################################################
### 2. 상태(state) update하기 - 수동으로
### update_state 사용, 새 메시지 추가
print('2.', '-' * 50)
##################################################################################
from langchain_core.messages import HumanMessage

_ = app.update_state(config, {"messages": [HumanMessage("Test")]})

state = app.get_state(config).values

print(f'Language: {state["language"]}')
for message in state["messages"]:
    message.pretty_print()
# 2. --------------------------------------------------
# Language: Spanish
# ================================ Human Message =================================

# Hi, I'm Bob.
# ================================== Ai Message ==================================

# ¡Hola, Bob! ¿Cómo puedo ayudarte hoy?
# ================================ Human Message =================================

# Test    