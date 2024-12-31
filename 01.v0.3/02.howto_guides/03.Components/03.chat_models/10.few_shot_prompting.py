from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool


@tool
def add(a: int, b: int) -> int:
    """Adds a and b."""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiplies a and b."""
    return a * b


tools = [add, multiply]


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm_with_tools = llm.bind_tools(tools)


#################################################################################
### 1. Tool calls - 연산 순서의 혼란
### 119*8의 값을 모르는 상태에서 add 도구를 호출 할 수 없음.
print('1.', '-' * 50)
##################################################################################
rprint(llm_with_tools.invoke(
    "Whats 119 times 8 minus 20. Don't do any math yourself, only use tools for math. Respect order of operations"
).tool_calls)
# 1. --------------------------------------------------
# [{'name': 'multiply', 'args': {'a': 119, 'b': 8}, 'id': 'call_Qe2YRI4AfdaLWcm3UTdmF8BK', 'type': 'tool_call'}, {'name': 'add', 'args': {'a': -20, 'b': 0}, 'id': 'call_ptiyjiGa9YRpSlzZHQqCnC00', 'type': 'tool_call'}]


#################################################################################
### 2. few shot prompting - 연산 순서의 예시
### 원하는 결과대로 나오지 않는 듯.
print('2.', '-' * 50)
##################################################################################
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

examples = [
    HumanMessage(
        "What's the product of 317253 and 128472 plus four", name="example_user"
    ),
    AIMessage(
        "",
        name="example_assistant",
        tool_calls=[
            {"name": "Multiply", "args": {"x": 317253, "y": 128472}, "id": "1"}
        ],
    ),
    ToolMessage("16505054784", tool_call_id="1"),
    AIMessage(
        "",
        name="example_assistant",
        tool_calls=[{"name": "Add", "args": {"x": 16505054784, "y": 4}, "id": "2"}],
    ),
    ToolMessage("16505054788", tool_call_id="2"),
    AIMessage(
        "The product of 317253 and 128472 plus four is 16505054788",
        name="example_assistant",
    ),
]

system = """You are bad at math but are an expert at using a calculator. 

Use past tool usage as an example of how to correctly use the tools."""
few_shot_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        *examples,
        ("human", "{query}"),
    ]
)

chain = {"query": RunnablePassthrough()} | few_shot_prompt | llm_with_tools
rprint(chain.invoke("Whats 119 times 8 minus 20").tool_calls)
# 2. --------------------------------------------------
# [{'name': 'multiply', 'args': {'a': 119, 'b': 8}, 'id': 'call_O6kph7mfuF3EtVZD6HVwyuYI', 'type': 'tool_call'}, {'name': 'add', 'args': {'a': -20, 'b': 0}, 'id': 'call_Hyx8lw1INZGuLy7xCgX6dMVf', 'type': 'tool_call'}]