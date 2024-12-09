from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo")

# Define tool
from langchain_core.tools import tool


@tool
def complex_tool(int_arg: int, float_arg: float, dict_arg: dict) -> int:
    """Do something complex with a complex tool."""
    return int_arg * float_arg

llm_with_tools = llm.bind_tools(
    [complex_tool],
)

### 1. error 발생
# Define chain
chain = llm_with_tools | (lambda msg: msg.tool_calls[0]["args"]) | complex_tool

### 아래는 테스트 후에 주석 처리 할 것 - 다음 코드가 실행 되도록
## print(chain.invoke("use complex tool. the args are 5, 2.1, empty dictionary. don't forget dict_arg"))
# pydantic.v1.error_wrappers.ValidationError: 1 validation error for complex_toolSchema
# dict_arg
#   field required (type=value_error.missing)


### 2. Try/except tool call
print('-'*30)
from typing import Any

from langchain_core.runnables import Runnable, RunnableConfig


def try_except_tool(tool_args: dict, config: RunnableConfig) -> Runnable:
    try:
        complex_tool.invoke(tool_args, config=config)
    except Exception as e:
        return f"Calling tool with arguments:\n\n{tool_args}\n\nraised the following error:\n\n{type(e)}: {e}"


chain = llm_with_tools | (lambda msg: msg.tool_calls[0]["args"]) | try_except_tool
print(chain.invoke("use complex tool. the args are 5, 2.1, empty dictionary. don't forget dict_arg"))
# Calling tool with arguments:

# {'int_arg': 5, 'float_arg': 2.1}

# raised the following error:

# <class 'pydantic.v1.error_wrappers.ValidationError'>: 1 validation error for complex_toolSchema
# dict_arg
#   field required (type=value_error.missing)


### 3. Fallbacks
print('-'*30)
chain = llm_with_tools | (lambda msg: msg.tool_calls[0]["args"]) | complex_tool
better_model = ChatOpenAI(model="gpt-4-1106-preview", temperature=0).bind_tools(
    [complex_tool], tool_choice="complex_tool"
)
better_chain = better_model | (lambda msg: msg.tool_calls[0]["args"]) | complex_tool

chain_with_fallback = chain.with_fallbacks([better_chain])
print(chain_with_fallback.invoke("use complex tool. the args are 5, 2.1, empty dictionary. don't forget dict_arg"))
# 10.5
### 'gpt-4-1106-preview': 정상 작동 / 'gpt-4', 'gpt-4o': error 발생


### 4. Retry with exception
print('-'*30)
import json
from typing import Any

from langchain_core.messages import AIMessage, HumanMessage, ToolCall, ToolMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough


class CustomToolException(Exception):
    """Custom LangChain tool exception."""

    def __init__(self, tool_call: ToolCall, exception: Exception) -> None:
        super().__init__()
        self.tool_call = tool_call
        self.exception = exception


def tool_custom_exception(msg: AIMessage, config: RunnableConfig) -> Runnable:
    try:
        return complex_tool.invoke(msg.tool_calls[0]["args"], config=config)
    except Exception as e:
        raise CustomToolException(msg.tool_calls[0], e)


def exception_to_messages(inputs: dict) -> dict:
    exception = inputs.pop("exception")

    # Add historical messages to the original input, so the model knows that it made a mistake with the last tool call.
    messages = [
        AIMessage(content="", tool_calls=[exception.tool_call]),
        ToolMessage(
            tool_call_id=exception.tool_call["id"], content=str(exception.exception)
        ),
        HumanMessage(
            content="The last tool call raised an exception. Try calling the tool again with corrected arguments. Do not repeat mistakes."
        ),
    ]
    inputs["last_output"] = messages
    return inputs


# We add a last_output MessagesPlaceholder to our prompt which if not passed in doesn't
# affect the prompt at all, but gives us the option to insert an arbitrary list of Messages
# into the prompt if needed. We'll use this on retries to insert the error message.
prompt = ChatPromptTemplate.from_messages(
    [("human", "{input}"), MessagesPlaceholder("last_output", optional=True)]
)
chain = prompt | llm_with_tools | tool_custom_exception

# If the initial chain call fails, we rerun it withe the exception passed in as a message.
self_correcting_chain = chain.with_fallbacks([exception_to_messages | chain], exception_key="exception")
print(self_correcting_chain.invoke({"input": "use complex tool. the args are 5, 2.1, empty dictionary. don't forget dict_arg"}))
# 10.5