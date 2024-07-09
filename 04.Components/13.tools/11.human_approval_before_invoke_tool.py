from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo")

from typing import Dict, List

from langchain_core.messages import AIMessage
from langchain_core.runnables import Runnable, RunnablePassthrough
from langchain_core.tools import tool


@tool
def count_emails(last_n_days: int) -> int:
    """Multiply two integers together."""
    print(f'count_emails: {last_n_days}')
    return last_n_days * 2


@tool
def send_email(message: str, recipient: str) -> str:
    """Add two integers."""
    print(f'send_email: {message}, {recipient}')
    return f"Successfully sent email to {recipient}."


tools = [count_emails, send_email]
llm_with_tools = llm.bind_tools(tools)


def call_tools(msg: AIMessage) -> List[Dict]:
    """Simple sequential tool calling helper."""
    tool_map = {tool.name: tool for tool in tools}
    tool_calls = msg.tool_calls.copy()
    for tool_call in tool_calls:
        tool_call["output"] = tool_map[tool_call["name"]].invoke(tool_call["args"])
    return tool_calls


### 1. 도구 호출하기
chain = llm_with_tools | call_tools
print(chain.invoke("how many emails did i get in the last 5 days?"))
# count_emails: 5
# [{'name': 'count_emails', 'args': {'last_n_days': 5}, 'id': 'call_oEZLRIIIYphOyOb7muPrNd6t', 'output': 10}]


### 2. 사용자 승인 추가하기
print('-'*30)
import json


class NotApproved(Exception):
    """Custom exception."""


def human_approval(msg: AIMessage) -> AIMessage:
    """Responsible for passing through its input or raising an exception.

    Args:
        msg: output from the chat model

    Returns:
        msg: original output from the msg
    """
    tool_strs = "\n\n".join(
        json.dumps(tool_call, indent=2) for tool_call in msg.tool_calls
    )
    input_msg = (
        f"Do you approve of the following tool invocations\n\n{tool_strs}\n\n"
        "Anything except 'Y'/'Yes' (case-insensitive) will be treated as a no.\n >>>"
    )
    resp = input(input_msg)
    if resp.lower() not in ("yes", "y"):
        raise NotApproved(f"Tool invocations not approved:\n\n{tool_strs}")
    return msg

chain = llm_with_tools | human_approval | call_tools
print(chain.invoke("how many emails did i get in the last 5 days?"))
# Do you approve of the following tool invocations

# {
#   "name": "count_emails",
#   "args": {
#     "last_n_days": 5
#   },
#   "id": "call_E7cZYpXXCOS6nwvU6MLYzwaJ"
# }

# Anything except 'Y'/'Yes' (case-insensitive) will be treated as a no.
#  >>>

### y
# count_emails: 5
# [{'name': 'count_emails', 'args': {'last_n_days': 5}, 'id': 'call_DnaLYByqiOoeK9nsCMmBM4db', 'output': 10}]

### n
# NotApproved: Tool invocations not approved:

# {
#   "name": "count_emails",
#   "args": {
#     "last_n_days": 5
#   },
#   "id": "call_E7cZYpXXCOS6nwvU6MLYzwaJ"
# }