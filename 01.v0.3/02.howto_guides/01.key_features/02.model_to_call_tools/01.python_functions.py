# The function name, type hints, and docstring are all part of the tool
# schema that's passed to the model. Defining good, descriptive schemas
# is an extension of prompt engineering and is an important part of
# getting models to perform well.
def add(a: int, b: int) -> int:
    """Add two integers.

    Args:
        a: First integer
        b: Second integer
    """
    print('Called add with', a, 'and', b)
    return a + b


def multiply(a: int, b: int) -> int:
    """Multiply two integers.

    Args:
        a: First integer
        b: Second integer
    """
    print(f'Called multiply with {a} and {b}')
    return a * b

tools = [add, multiply]

##################################################################################
### 1. Tool calls
print('1.', '-' * 50)
##################################################################################
from langchain_openai import ChatOpenAI
from rich import print as rprint

llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools)

query = "What is 3 * 12?"
results = llm_with_tools.invoke(query)
rprint(results)
# AIMessage(
#     content='',
#     additional_kwargs={
#         'tool_calls': [{'id': 'call_gIZZghxh52bbr3PzD6bmTKfp', 'function': {'arguments': '{"a":3,"b":12}', 'name': 'multiply'}, 'type': 'function'}],
#         'refusal': None
#     },
#     response_metadata={
#         'token_usage': {
#             'completion_tokens': 17,
#             'prompt_tokens': 87,
#             'total_tokens': 104,
#             'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0},
#             'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}
#         },
#         'model_name': 'gpt-4o-mini-2024-07-18',
#         'system_fingerprint': 'fp_bba3c8e70b',
#         'finish_reason': 'tool_calls',
#         'logprobs': None
#     },
#     id='run-b8ee9057-c9ae-4a0f-8c77-aeab5f9c69c9-0',
#     tool_calls=[{'name': 'multiply', 'args': {'a': 3, 'b': 12}, 'id': 'call_gIZZghxh52bbr3PzD6bmTKfp', 'type': 'tool_call'}],
#     usage_metadata={
#         'input_tokens': 87,
#         'output_tokens': 17,
#         'total_tokens': 104,
#         'input_token_details': {'audio': 0, 'cache_read': 0},
#         'output_token_details': {'audio': 0, 'reasoning': 0}
#     }
# )


##################################################################################
### 2. Parsing - PydanticToolsParser 사용
print('2.', '-' * 50)
##################################################################################
from langchain_core.output_parsers import PydanticToolsParser
from pydantic import BaseModel, Field

class add(BaseModel):
    """Add two integers."""

    a: int = Field(..., description="First integer")
    b: int = Field(..., description="Second integer")


class multiply(BaseModel):
    """Multiply two integers."""

    a: int = Field(..., description="First integer")
    b: int = Field(..., description="Second integer")    

chain = llm_with_tools | PydanticToolsParser(tools=[add, multiply])
results = chain.invoke(query)
rprint(results)
# 2. --------------------------------------------------
# [multiply(a=3, b=12)]

