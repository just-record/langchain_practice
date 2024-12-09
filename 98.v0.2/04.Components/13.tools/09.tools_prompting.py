
### 1. 도구 호출이 지원 되지 않는 local 모델 사용
### 자신만의 local 모델 사용 - <https://python.langchain.com/v0.2/docs/integrations/chat/ollama/>
### local model을 구축 하지 않는 이상 아래 소스 코드는 실행이 안됨
# from langchain_community.llms import Ollama

# model = Ollama(model="phi3")

from langchain_openai import ChatOpenAI

model = ChatOpenAI(
                model='EEVE-Korean-Instruct-10.8B-v1.0-gguf',
                api_key='lm-studio',
                base_url='http://111.111.111.111:1234/v1',
                temperature=0
            ) 

### 2. Create a tool
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
    print("--")
    print(t.name)
    print(t.description)
    print(t.args)
# --
# multiply
# Multiply two numbers together.
# {'x': {'title': 'X', 'type': 'number'}, 'y': {'title': 'Y', 'type': 'number'}}
# --
# add
# Add two numbers.
# {'x': {'title': 'X', 'type': 'integer'}, 'y': {'title': 'Y', 'type': 'integer'}}


### 3. Creating our prompt
print('-'*30)
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import render_text_description

rendered_tools = render_text_description(tools)
print(rendered_tools)
# multiply(x: float, y: float) -> float - Multiply two numbers together.
# add(x: int, y: int) -> int - Add two numbers.

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

chain = prompt | model
message = chain.invoke({"input": "what's 3 plus 1132"})

print('-'*30)
# Let's take a look at the output from the model
# if the model is an LLM (not a chat model), the output will be a string.
if isinstance(message, str):
    print(message)
    # { "name": "add", "arguments": { "x": 3, "y": 1132 } }
else:  # Otherwise it's a chat model
    print(message.content)


### 4. Adding an output parser
print('-'*30)
from langchain_core.output_parsers import JsonOutputParser

chain = prompt | model | JsonOutputParser()
print(chain.invoke({"input": "what's thirteen times 4"}))
# {'name': 'multiply', 'arguments': {'x': 13, 'y': 4}}


### 5. Invoking the tool
print('-'*30)
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

print(invoke_tool({"name": "multiply", "arguments": {"x": 3, "y": 5}}))
# 15.0


### 6. Let's put it together
print('-'*30)
chain = prompt | model | JsonOutputParser() | invoke_tool
print(chain.invoke({"input": "what's thirteen times 4.14137281"}))
# 53.83784653


### 7. Returning tool inputs
# tool의 input 값도 같이 반환하게 만들기
print('-'*30)
from langchain_core.runnables import RunnablePassthrough

chain = (
    prompt | model | JsonOutputParser() | RunnablePassthrough.assign(output=invoke_tool)
)
print(chain.invoke({"input": "what's thirteen times 4.14137281"}))
# {'name': 'multiply', 'arguments': {'x': 13, 'y': 4.14137281}, 'output': 53.83784653}