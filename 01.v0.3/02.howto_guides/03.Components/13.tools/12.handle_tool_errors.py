from dotenv import load_dotenv
load_dotenv()
from rich import print as rprint

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")


### Tool 정의 ###
# Define tool
from langchain_core.tools import tool


@tool
def complex_tool(int_arg: int, float_arg: float, dict_arg: dict) -> int:
    """Do something complex with a complex tool."""
    return int_arg * float_arg


llm_with_tools = llm.bind_tools(
    [complex_tool],
)

### Chain 정의 ###
# Define chain
chain = llm_with_tools | (lambda msg: msg.tool_calls[0]["args"]) | complex_tool


#################################################################################
### 1. Chain invoke - complex tool 호출 => 오류 발생
### 코드는 다음 코드를 실행하기 위해 주석 처리
print('1.', '-' * 50)
################################################################################## 
# rprint(chain.invoke("use complex tool. the args are 5, 2.1, empty dictionary. don't forget dict_arg"))
# 1. --------------------------------------------------
# pydantic_core._pydantic_core.ValidationError: 1 validation error for complex_tool
# dict_arg
#   Field required [type=missing, input_value={'int_arg': 5, 'float_arg': 2.1}, input_type=dict]
#     For further information visit https://errors.pydantic.dev/2.10/v/missing


#################################################################################
### 2. Try/except tool call
### 오류가 발생하면 도움이 되는 message를 반환
print('2.', '-' * 50)
################################################################################## 
from typing import Any

from langchain_core.runnables import Runnable, RunnableConfig


def try_except_tool(tool_args: dict, config: RunnableConfig) -> Runnable:
    try:
        complex_tool.invoke(tool_args, config=config)
    except Exception as e:
        return f"Calling tool with arguments:\n\n{tool_args}\n\nraised the following error:\n\n{type(e)}: {e}"


chain = llm_with_tools | (lambda msg: msg.tool_calls[0]["args"]) | try_except_tool

rprint(chain.invoke("use complex tool. the args are 5, 2.1, empty dictionary. don't forget dict_arg"))
# 2. --------------------------------------------------
# Calling tool with arguments:

# {'int_arg': 5, 'float_arg': 2.1}

# raised the following error:

# <class 'pydantic_core._pydantic_core.ValidationError'>: 1 validation error for complex_tool
# dict_arg
#   Field required 
#     For further information visit https://errors.pydantic.dev/2.10/v/missing


#################################################################################
### 3. Fallbacks
### 오류가 발생하면 도움이 되는 message를 반환
print('3.', '-' * 50)
################################################################################## 
chain = llm_with_tools | (lambda msg: msg.tool_calls[0]["args"]) | complex_tool

model = "gpt-4-turbo" # "gpt-4-turbo", "gpt-4o" => "gpt-4-turbo" 만 사용 가능
better_model = ChatOpenAI(model=model, temperature=0).bind_tools(
    [complex_tool], tool_choice="complex_tool"
)

better_chain = better_model | (lambda msg: msg.tool_calls[0]["args"]) | complex_tool

chain_with_fallback = chain.with_fallbacks([better_chain])

rprint(chain_with_fallback.invoke("use complex tool. the args are 5, 2.1, empty dictionary. don't forget dict_arg"))
# 3. --------------------------------------------------
# 10.5


#################################################################################
### 4. Retry with exception
### 예외 상황을 자동으로 체인에 다시 전달하여 실행함으로써 모델이 자신의 동작을 수정
print('4.', '-' * 50)
################################################################################## 
from langchain_core.messages import AIMessage, HumanMessage, ToolCall, ToolMessage
from langchain_core.prompts import ChatPromptTemplate


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
    [("human", "{input}"), ("placeholder", "{last_output}")]
)
chain = prompt | llm_with_tools | tool_custom_exception

# If the initial chain call fails, we rerun it withe the exception passed in as a message.
self_correcting_chain = chain.with_fallbacks(
    [exception_to_messages | chain], exception_key="exception"
)

#################################################################################
# exception_key="exception"는 체인의 오류 처리 메커니즘에서 중요한 역할을 합니다.
# 이 파라미터는 .with_fallbacks() 메서드에서 사용

# 체인 실행 중 발생하는 예외를 어떤 키로 저장하고 전달할지 지정합니다.
# 코드에서는 "exception"이라는 키를 사용하여, 발생한 예외를 exception_to_messages 함수로 전달합니다.
# exception_to_messages 함수는 이 exception 키를 통해 전달받은 예외 정보를 사용하여:

# 예외가 발생한 도구 호출 정보
# 실제 예외 내용
# 수정을 요청하는 메시지

# 즉, exception_key="exception"은 예외 처리 시스템에서 예외 정보를 전달하는 식별자 역할을 하며, 이를 통해 체인이 자동으로 오류를 수정하고 재시도할 수 있게 됩니다
#################################################################################

results = self_correcting_chain.invoke(
    {
        "input": "use complex tool. the args are 5, 2.1, empty dictionary. don't forget dict_arg"
    }
)
rprint(results)
# 4. --------------------------------------------------
# 10.5