# pip install --upgrade --quiet langchain langchain-community

# 일부 모델은 도구 호출을 위해 미세 조정되었으며 도구 호출을 위한 전용 API를 제공합니다. 
# 일반적으로 이러한 모델들은 미세 조정되지 않은 모델보다 도구 호출에 더 적합하며, 도구 호출이 필요한 사용 사례에 권장됩니다.

# 도구 호출을 기본적으로 지원하지 않는 모델을 사용할 때 도구를 호출하는 대체 방법입니다.
# 이는 모델이 적절한 도구를 호출하도록 하는 프롬프트를 작성하는 것만으로 가능합니다.

from rich import print as rprint
from langchain_community.llms import Ollama

### phi3은 도구 호출을 지원하지 않는 모델입니다.
model = Ollama(model="phi3")


#################################################################################
### 1. Create a tool
print('1.', '-' * 50)
#################################################################################
from langchain_core.tools import tool


@tool
def multiply(x: float, y: float) -> float:
    """Multiply two numbers together."""
    return x * y


@tool
def add(x: int, y: int) -> int:
    "Add two numbers."
    return x + y


tools = [multiply, add]

# Let's inspect the tools
for t in tools:
    print("****")
    print(t.name)
    print(t.description)
    print(t.args)
# 1. --------------------------------------------------
# ****
# multiply
# Multiply two numbers together.
# {'x': {'title': 'X', 'type': 'number'}, 'y': {'title': 'Y', 'type': 'number'}}
# ****
# add
# Add two numbers.
# {'x': {'title': 'X', 'type': 'integer'}, 'y': {'title': 'Y', 'type': 'integer'}}

    
### invoke ###
print(' ')
rprint(multiply.invoke({"x": 4, "y": 5})    )
# 20.0    


#################################################################################
### 2. Creating our prompt
### 모델이 접근할 수 있는 도구들, 해당 도구들의 인자값들, 그리고 모델의 원하는 출력 형식을 지정하는 프롬프트를 작성
### 모델이 {"name": "...", "arguments": ...} 형식의 JSON 블롭을 출력하도록 지시
#################################################################################
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import render_text_description


#################################################################################
### 2-1. Render the tools - 'render_text_description'사용 -> 결과 참조
print('2-1.', '-' * 50)
#################################################################################
rendered_tools = render_text_description(tools)
rprint(rendered_tools)
# 2. --------------------------------------------------
# multiply(x: float, y: float) -> float - Multiply two numbers together.
# add(x: int, y: int) -> int - Add two numbers.


#################################################################################
### 2-2. Render된 tool 내용을 JSON blob으로 반환하는 프롬프트 작성
print('2-2.', '-' * 50)
#################################################################################
system_prompt = f"""\
You are an assistant that has access to the following set of tools. 
Here are the names and descriptions for each tool:

{rendered_tools}

Given the user input, return the name and input of the tool to use. 
Return your response as a JSON blob with 'name' and 'arguments' keys.

The `arguments` should be a dictionary, with keys corresponding 
to the argument names and the values corresponding to the requested values.
"""

prompt = ChatPromptTemplate.from_messages(
    [("system", system_prompt), ("user", "{input}")]
)
rprint(prompt.messages[0].prompt.template)
# 2-2. --------------------------------------------------
# You are an assistant that has access to the following set of tools. 
# Here are the names and descriptions for each tool:

# multiply(x: float, y: float) -> float - Multiply two numbers together.
# add(x: int, y: int) -> int - Add two numbers.

# Given the user input, return the name and input of the tool to use. 
# Return your response as a JSON blob with 'name' and 'arguments' keys.

# The `arguments` should be a dictionary, with keys corresponding 
# to the argument names and the values corresponding to the requested values.


#################################################################################
### 2-3. model과 chaining 하고 chain invoke
print('2-3.', '-' * 50)
#################################################################################
chain = prompt | model
message = chain.invoke({"input": "what's 3 plus 1132"})

# Let's take a look at the output from the model
# if the model is an LLM (not a chat model), the output will be a string.
# rprint(message)
if isinstance(message, str):
    print(message)
else:  # Otherwise it's a chat model
    print(message.content)
# 2-3. --------------------------------------------------
# {
#   "name": "add",
#   "arguments": {
#     "x": 3,
#     "y": 1132
#   }
# }    


#################################################################################
### 3. Adding an output parser
### output을 JSON 으로 파싱 - 'JsonOutputParser' 사용
print('3.', '-' * 50)
#################################################################################
from langchain_core.output_parsers import JsonOutputParser

chain = prompt | model | JsonOutputParser()
rprint(chain.invoke({"input": "what's thirteen times 4"}))
# 3. --------------------------------------------------
# {'name': 'multiply', 'arguments': {'x': 13, 'y': 4}}


#################################################################################
### 4. Invoking the tool
### 모델이 도구를 호출할 수 있게 되었으므로, 실제로 도구를 호출할 수 있는 함수를 작성
### 이 함수는 이름으로 적절한 도구를 선택하고, 모델이 선택한 인자들을 해당 도구에 전달
print('4.', '-' * 50)
#################################################################################
from typing import Any, Dict, Optional, TypedDict

from langchain_core.runnables import RunnableConfig


class ToolCallRequest(TypedDict):
    """A typed dict that shows the inputs into the invoke_tool function."""

    name: str
    arguments: Dict[str, Any]


def invoke_tool(
    tool_call_request: ToolCallRequest, config: Optional[RunnableConfig] = None
):
    """A function that we can use the perform a tool invocation.

    Args:
        tool_call_request: a dict that contains the keys name and arguments.
            The name must match the name of a tool that exists.
            The arguments are the arguments to that tool.
        config: This is configuration information that LangChain uses that contains
            things like callbacks, metadata, etc.See LCEL documentation about RunnableConfig.

    Returns:
        output from the requested tool
    """
    tool_name_to_tool = {tool.name: tool for tool in tools}
    name = tool_call_request["name"]
    requested_tool = tool_name_to_tool[name]
    return requested_tool.invoke(tool_call_request["arguments"], config=config)

### tool invo0ke ###
rprint(invoke_tool({"name": "multiply", "arguments": {"x": 3, "y": 5}}))
# 4. --------------------------------------------------
# 15.0


#################################################################################
### 5. Let's put it together
### 생성된 chain은 더하기와 곱하기를 계산 할 수 있는 계산기
print('5.', '-' * 50)
#################################################################################
chain = prompt | model | JsonOutputParser() | invoke_tool
rprint(chain.invoke({"input": "what's thirteen times 4.14137281"}))
# 5. --------------------------------------------------
# 53.83784653

#################################################################################
### 6. Returning tool inputs
### tool input을 반환 - 'RunnablePassthrough.assign' 사용
print('6.', '-' * 50)
#################################################################################
from langchain_core.runnables import RunnablePassthrough

chain = (
    prompt | model | JsonOutputParser() | RunnablePassthrough.assign(output=invoke_tool)
)
rprint(chain.invoke({"input": "what's thirteen times 4.14137281"}))
# 6. --------------------------------------------------
# {'name': 'multiply', 'arguments': {'x': 13, 'y': 4.14137281}, 'output': 53.83784653}