# 모델이 단독으로 실행하기에 신뢰할 수 없는 도구들이 있을 때 도구가 실행되기 전에 사람의 승인 받기

from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

from typing import Dict, List

from langchain_core.messages import AIMessage
from langchain_core.runnables import Runnable, RunnablePassthrough
from langchain_core.tools import tool


#################################################################################
### 1. Chain 만들기
### Dummy tools and tool-calling chain
################################################################################## 
@tool
def count_emails(last_n_days: int) -> int:
    """Dummy function to count number of e-mails. Returns 2 * last_n_days."""
    return last_n_days * 2


@tool
def send_email(message: str, recipient: str) -> str:
    """Dummy function for sending an e-mail."""
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


#################################################################################
### chain invoke - 지난 5일 동안 받은 이메일 수(도구를 호출 하여 결과를 얻음)
print('1.', '-' * 50)
################################################################################## 
chain = llm_with_tools | call_tools
rprint(chain.invoke("how many emails did i get in the last 5 days?"))
# 1. --------------------------------------------------
# [{'name': 'count_emails', 'args': {'last_n_days': 5}, 'id': 'call_fcmKC2JE3ZtyLRFV0VR4VRit', 'type': 'tool_call', 'output': 10}]



#################################################################################
### 2. 사용자 승인 추가하기
### 반려시 오류가 발생 - chain의 남은 부분은 실행되지 않음
################################################################################## 
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


#################################################################################
### 2-1. 사용자에게 승인 요청
print('2-1.', '-' * 50)
################################################################################## 
chain = llm_with_tools | human_approval | call_tools
rprint(chain.invoke("how many emails did i get in the last 5 days?"))
# 2-1. --------------------------------------------------
# Do you approve of the following tool invocations

# {
#   "name": "count_emails",
#   "args": {
#     "last_n_days": 5
#   },
#   "id": "call_16pVxtEb1btm5SeUl69iTgQb",
#   "type": "tool_call"
# }

# Anything except 'Y'/'Yes' (case-insensitive) will be treated as a no.
#  >>>

#################################################################################
### 2-1-1. Y/Yes
################################################################################## 
# [{'name': 'count_emails', 'args': {'last_n_days': 5}, 'id': 'call_LFPKGkXEuX8GRMTLjxGPIZxA', 'type': 'tool_call', 'output': 10}]

#################################################################################
### 2-1-2. N/No
################################################################################## 
# Traceback (most recent call last):
# ...
# NotApproved: Tool invocations not approved:

# {
#   "name": "count_emails",
#   "args": {
#     "last_n_days": 5
#   },
#   "id": "call_DZf4GhYc56Po3cv6WlXi95t1",
#   "type": "tool_call"
# }